import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, NoReturn, Optional

import click
from cognite.client import CogniteClient
from cognite.client.data_classes import DataSet
from google.api_core.exceptions import NotFound
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage
from google.cloud.secretmanager import SecretManagerServiceClient
from termcolor import cprint

from forge_template.handler.sa_file_handler import CustomReplicatorFileHandler, Env, ExtractorWorkflowFileHandler
from forge_template.paths import (
    CR_GCP_CONFIG_PATH,
    CR_OUTPUT_DIR,
    DATA_REPLICATOR_OUTPUT_DIR,
    EW_GCP_CONFIG_PATH,
    EW_OUTPUT_DIR,
)
from forge_template.sa_constants import (
    CDF_API_HOST_REGEX,
    DATA_TYPE_OPTIONS,
    DEFAULT_CDF_API_HOST,
    DOC_URL,
    GCP_PROJECT_NAME,
    GS_SERVICE_ACCOUNTS,
    JOB_CONFIGS_BUCKET,
    SCHEDULE_OPTIONS,
)
from forge_template.user_interface import UserInterface
from forge_template.util.log_util import print_goodbye
from forge_template.util.sa_util import get_utc_timestamp_as_str, print_monitor_replication

logger = logging.getLogger(__file__)


@dataclass
class CDFInfo:
    name: str
    key: str
    client: CogniteClient


def generate_data_replication() -> None:
    """
    Kicks off "Generate a custom data replication"
    """
    ui = UserInterface()

    try:
        secret_manager_client = SecretManagerServiceClient()
    except DefaultCredentialsError as e:
        handle_default_credentials_error(e)

    # Request tenant information
    while True:
        tenant_names = get_tenant_names_data_replication()
        tenant_info = get_tenant_info(secret_manager_client, tenant_names, ui)
        if tenant_info:
            break

    sync_path = CR_GCP_CONFIG_PATH / f"{tenant_names[Env.SRC]}-{tenant_names[Env.DST]}"
    sync_local_directory(sync_path)

    # Request replication information
    data_type = ui.choose_option(prompt="Which data type do you want to replicate?", options=DATA_TYPE_OPTIONS)
    schedule = ui.choose_option(prompt="How often should the data be replicated", options=SCHEDULE_OPTIONS)
    cdf_api_hosts = request_cdf_api_hosts()
    job_id = ""
    while not job_id:
        job_id = click.prompt(f"Please choose a name / id for the replication job")
        if does_job_id_exist(
            job_id=job_id, src_tenant=tenant_names[Env.SRC], dst_tenant=tenant_names[Env.DST], data_type=data_type
        ):
            cprint(f'The chosen job id "{job_id}" already exists.', "red")
            if not click.confirm("Do you want to overwrite the existing job?"):
                job_id = ""

    # Generate job config
    job_config_generated = False
    while not job_config_generated:
        file_handler = CustomReplicatorFileHandler(
            data_type=data_type,
            schedule=schedule,
            tenant_names=tenant_names,
            cdf_api_hosts=cdf_api_hosts,
            job_id=job_id,
        )
        cprint("Please specify the replication details:", color="blue")
        file_handler.generate_job_config()
        file_handler.config_generator.preview()
        if click.confirm("Please check your input once again. Are you satisfied with the shown preview?"):
            file_handler.config_generator.save()
            job_config_generated = True
        else:
            job_config_generated = False
    file_handler.generate_schedule()
    file_handler.upload_configs_to_gcp()
    cprint(
        f"Successfully activated replication of {data_type} from {tenant_names[Env.SRC]} to {tenant_names[Env.DST]}",
        "green",
    )
    print_monitor_replication()


def extractor_workflow():
    """
    Kicks off "Set up extractor workflow"
    """
    ui = UserInterface()

    try:
        secret_manager_client = SecretManagerServiceClient()
    except DefaultCredentialsError as e:
        handle_default_credentials_error(e)

    while True:
        tenant_names = get_tenant_names_extractor_workflow(ui)
        base_tenant = tenant_names.pop(Env.BASE)
        tenant_info = get_tenant_info(secret_manager_client, tenant_names, ui)
        if type(tenant_info) is dict:
            break

    sync_path = EW_GCP_CONFIG_PATH / f"{base_tenant}"
    sync_local_directory(sync_path)

    options = {
        "Work on a new extractor": lambda: new_extractor(tenant_info, base_tenant, ui),
        "Update an existing extractor": lambda: update_extractor(tenant_info, base_tenant, ui),
    }

    ui.show_menu("What do you want to do?", options)


def sync_local_directory(directory: Path):
    """
    Syncs the local directory for storing the config files with the remote one

    Parameters:
         directory(str): which directory to sync. Should be either "custom_replicator" or "extractor_workflow"
    """
    try:
        storage_client = storage.Client()
    except DefaultCredentialsError as e:
        handle_default_credentials_error(e)

    cprint(f"Start syncing local with remote repository: {directory}", "blue")
    bucket_name = JOB_CONFIGS_BUCKET
    prefix = directory
    local_base_dir = DATA_REPLICATOR_OUTPUT_DIR

    blobs = storage_client.list_blobs(bucket_name, prefix=str(prefix))
    download_count = 0
    for blob in blobs:
        file_split = blob.name.split("/")
        file_directory = "/".join(file_split[:-1])
        Path(local_base_dir, file_directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(Path(local_base_dir, blob.name))
        download_count += 1

    if download_count:
        cprint(f"Successfully synced {download_count} files from remote repository", "green")
    else:
        cprint(f"Remote repository seems empty!", "yellow")


def new_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface) -> None:
    """
    Kicks off "Work on a new extractor"

    Parameters:
        tenant_info (Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
    """
    options = {
        f"Start work on a new extractor on {tenant_info[Env.DEV].name}": lambda: start_new_extractor(
            tenant_info, base_tenant, ui
        ),
        f"Test new extractor on {tenant_info[Env.TEST].name}": lambda: test_new_extractor(tenant_info, base_tenant, ui),
        f"Deploy new extractor to {tenant_info[Env.PROD].name}": lambda: deploy_new_extractor(
            tenant_info, base_tenant, ui
        ),
    }

    ui.show_menu("What do you want to do?", options)


def update_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface) -> None:
    """
    Kicks off "Update an existing extractor"

    Parameters:
        tenant_info (Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str)
        ui (UserInterface):
    """
    options = {
        f"Start work on updating an existing extractor on "
        f"{tenant_info[Env.DEV].name}": lambda: start_update_extractor(tenant_info, base_tenant, ui),
        f"Test updated extractor on {tenant_info[Env.TEST].name}": lambda: test_update_extractor(
            tenant_info, base_tenant, ui
        ),
        f"Deploy updated extractor to {tenant_info[Env.PROD].name}": lambda: deploy_update_extractor(
            tenant_info, base_tenant, ui
        ),
    }

    ui.show_menu("What do you want to do?", options)


def start_new_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface) -> None:
    """
    Kicks off "Start work on a new extractor on <tenant-dev>"

    Parameters:
        tenant_info (Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
    """
    start_extractor(tenant_info, base_tenant, ui, update=False)


def test_new_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface) -> None:
    """
    Kicks off "Test new extractor on <tenant-test>"

    Parameters:
        tenant_info (Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
    """
    test_extractor(tenant_info, base_tenant, ui, update=False)


def deploy_new_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface) -> None:
    """
    Kicks of "Deploy new extractor on <tenant-prod>"

    Parameters:
        tenant_info (Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
    """
    deploy_extractor(tenant_info, base_tenant, ui, update=False)


def start_update_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface) -> None:
    """
    Kicks off "Start work on updating an existing extractor on <tenant-dev>"

    Parameters:
        tenant_info(Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
    """
    start_extractor(tenant_info, base_tenant, ui, update=True)


def test_update_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant, ui: UserInterface) -> None:
    """
    Kicks off "Test an updated extractor on <tenant-dev>"

    Parameters:
        tenant_info(Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
    """
    test_extractor(tenant_info, base_tenant, ui, update=True)


def deploy_update_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface) -> None:
    """
    Kicks off "Deploy an updated extractor on <tenant-dev>"

    Parameters:
        tenant_info(Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
    """
    deploy_extractor(tenant_info, base_tenant, ui, update=True)


def start_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface, update: bool):
    """
    Guides the user through either
    1) Start working on a new extractor (update: False) or
    2) Start working on updating an existing extractor (update: True)
    Additionally, the necessary data replications are set up

    Parameters:
        tenant_info(Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
        update (bool): True for "update extractor" workflow, False for "new extractor" workflow
    """
    prod_tenant = tenant_info[Env.PROD].name
    dev_tenant = tenant_info[Env.DEV].name

    # Get extractor_id
    if update:
        try:
            extractor_options = get_extractor_names(location=Path(base_tenant, "prod-test", "deployed"))
            extractor_id = ui.choose_option(prompt="Choose extractor to deploy", options=extractor_options)
        except FileNotFoundError:
            cprint("There is no extractor to start updating. Please select another option.", "red")
            return
    else:
        extractor_id = click.prompt("Please enter external id of extractor / data set")

    # Handle information about which data sets to replicate
    while True:
        data_sets = click.prompt(
            f"Enter which data sets to replicate from {prod_tenant} to {dev_tenant} as a comma separated list"
        )
        data_sets = data_sets.replace(" ", "").split(",")
        invalid_data_sets = get_invalid_data_sets(data_sets, tenant_info[Env.PROD])
        if not invalid_data_sets:
            break
        cprint(f"The following data sets do not exist in {prod_tenant}: {invalid_data_sets}", "red")

    invalid_data_sets_dev = get_invalid_data_sets(data_sets, tenant_info[Env.DEV])
    if not does_data_set_exist(extractor_id, tenant_info[Env.DEV]):
        invalid_data_sets_dev.append(extractor_id)

    for data_set in invalid_data_sets_dev:
        create_data_set(data_set, tenant_info[Env.DEV])

    # Set up replication and store files in prod-dev/started
    schedule = ui.choose_option(prompt="How often should the data be replicated", options=SCHEDULE_OPTIONS)
    file_handler = ExtractorWorkflowFileHandler(base_tenant=base_tenant, extractor_id=extractor_id, schedule=schedule)
    file_handler.generate_config_files(
        data_sets_to_replicate=data_sets, src_env=Env.PROD, dst_env=Env.DEV, stage="started"
    )
    file_handler.activate_replication(src_env=Env.PROD, dst_env=Env.DEV, stage="started")

    # For updating existing extractor: move already existing config files
    if update:
        file_handler.move_folder_locally(src_env=Env.PROD, dst_env=Env.TEST, move_from="deployed", move_to="started")
        file_handler.move_folder_on_gcp(src_env=Env.PROD, dst_env=Env.TEST, move_from="deployed", move_to="started")

    # User guidance: remind to deploy new / updated extractor to development environment
    workflow_stage = "updated" if update else "new"
    cprint(f'Successfully activated the replication of {data_sets} from "{prod_tenant}" to "{dev_tenant}".', "green")
    print_monitor_replication()
    cprint(
        f'Now it is time to deploy the {workflow_stage} extractor towards "{dev_tenant}" and populate the data set '
        f'"{extractor_id}".',
        "yellow",
    )
    click.confirm("Hit enter to confirm deployment", show_default=False)

    # Finally, check for rollback of data replications towards dev-tenant
    rollback = check_for_rollback(tenant=dev_tenant, stage="started", update=update, file_handler=file_handler)

    if not rollback:
        s = "an updated" if update else "a new"
        cprint(
            f"Congratulations! You completed all steps to start working on {s} extractor. Now you can continue with "
            "the test step.",
            "green",
        )


def test_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface, update: bool):
    """
    Guides the user through either
    1) Test a new extractor (update: False) or
    2) Test an updated, existing extractor (update: True)


    Parameters:
        tenant_info(Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
        update (bool): True for "update extractor" workflow, False for "new extractor" workflow
    """
    test_tenant = tenant_info[Env.TEST].name

    # Get extractor name
    read_extractor_location = "prod-test" if update else "prod-dev"
    try:
        extractor_options = get_extractor_names(location=Path(base_tenant, read_extractor_location, "started"))
        extractor_id = ui.choose_option(prompt="Choose extractor to test", options=extractor_options)
    except FileNotFoundError:
        cprint("There is no extractor to test. Please select another option.", "red")
        return

    # Generate necessary data sets on test tenant
    if not does_data_set_exist(extractor_id, tenant_info[Env.TEST]):
        create_data_set(extractor_id, tenant_info[Env.TEST])

    # Move files from prod-dev/started -> prod-dev/tested
    file_handler = ExtractorWorkflowFileHandler(base_tenant=base_tenant, extractor_id=extractor_id)
    file_handler.move_folder_locally(src_env=Env.PROD, dst_env=Env.DEV, move_from="started", move_to="tested")
    file_handler.move_folder_on_gcp(src_env=Env.PROD, dst_env=Env.DEV, move_from="started", move_to="tested")

    # For updating existing extractor: deactivate replication for old extractor
    if update:
        file_handler.deactivate_replication(src_env=Env.PROD, dst_env=Env.TEST, move_from="started", move_to="tested")

    # User guidance: remind to deploy new / updated extractor to development environment
    workflow_stage = "updated" if update else "new"
    cprint(
        f"Please deploy your {workflow_stage} extractor towards your testing environment by "
        f'populating the data set "{extractor_id}" in "{tenant_info[Env.TEST].name}" with the {workflow_stage} '
        f"extractor. Further you have to deactivate the extractor into the development environment "
        f'"{tenant_info[Env.DEV].name}".',
        "yellow",
    )
    click.confirm(
        f"Once you have done both, hit enter to confirm", show_default=False,
    )

    # Finally, check for rollback of data replications towards dev-tenant
    rollback = check_for_rollback(tenant=test_tenant, stage="tested", update=update, file_handler=file_handler)

    if not rollback:
        s = "an updated" if update else "a new"
        cprint(
            f"Congratulations! You completed all steps to test {s} extractor. Now you can continue with the deploy "
            "step.",
            "green",
        )


def deploy_extractor(tenant_info: Dict[Env, CDFInfo], base_tenant: str, ui: UserInterface, update: bool):
    """
    Guides the user through either
    1) Deploy a new extractor (update: False) or
    2) Deploy an updated, existing extractor (update: True)
    Additionally, the necessary data replications are set up, and redundant data replications are deactivated


    Parameters:
        tenant_info(Dict[str, CDFInfo]): Dictionary with CDF tenant names and clients for each environment)
        base_tenant (str):
        ui (UserInterface):
        update (bool): True for "update extractor" workflow, False for "new extractor" workflow
    """
    test_tenant = tenant_info[Env.TEST].name
    prod_tenant = tenant_info[Env.PROD].name

    # Get extractor name
    read_extractor_location = "prod-test" if update else "prod-dev"
    try:
        extractor_options = get_extractor_names(location=Path(base_tenant, read_extractor_location, "tested"))
        extractor_id = ui.choose_option(prompt="Choose extractor to deploy", options=extractor_options)
    except FileNotFoundError:
        cprint("There is no extractor to deploy. Please select another option.", "red")
        return

    # Check if necessary data sets exist
    if not does_data_set_exist(extractor_id, tenant_info[Env.PROD]):
        create_data_set(extractor_id, tenant_info[Env.PROD])
    while not does_data_set_exist(extractor_id, tenant_info[Env.TEST]):
        cprint(f"There is no extractor {extractor_id} in {test_tenant}.", "red")
        click.confirm(
            "Please test new extractor first.", show_default=False,
        )
        test_new_extractor(tenant_info, base_tenant, ui)

    # Move files from prod-dev/tested -> prod-dev/deactivated and deploy new extractor on prod-test
    schedule = ui.choose_option(
        prompt=f'How often should the data from the extractor "{extractor_id}" be replicated in production?',
        options=SCHEDULE_OPTIONS,
    )
    file_handler = ExtractorWorkflowFileHandler(base_tenant=base_tenant, extractor_id=extractor_id, schedule=schedule)
    file_handler.generate_config_files(
        data_sets_to_replicate=[extractor_id], src_env=Env.PROD, dst_env=Env.TEST, stage="deployed"
    )
    file_handler.activate_replication(src_env=Env.PROD, dst_env=Env.TEST, stage="deployed")
    file_handler.deactivate_replication(src_env=Env.PROD, dst_env=Env.DEV, move_from="tested", move_to="deactivated")

    # For updating existing extractor: move already existing config files
    timestamp = get_utc_timestamp_as_str()
    if update:
        file_handler.move_folder_locally(
            src_env=Env.PROD, dst_env=Env.TEST, move_from="tested", move_to="deactivated", timestamp=timestamp,
        )
        file_handler.move_folder_on_gcp(
            src_env=Env.PROD, dst_env=Env.TEST, move_from="tested", move_to="deactivated", timestamp=timestamp,
        )

    cprint(f'The replication of "{extractor_id}" from "{prod_tenant}" to "{test_tenant}" is activated.', "green")
    print_monitor_replication()
    cprint(
        f'Now you have to develop your extractor towards your production environment by populating "{extractor_id}" in '
        f'"{prod_tenant}" with the new extractor. Further you have to deactivate the extractor into the testing '
        f"environment",
        "yellow",
    )
    click.confirm("Once you have done both, hit enter to confirm", show_default=False)
    s1 = "an updated" if update else "a new"
    s2 = "updated" if update else "new"
    cprint(
        f"Congratulations! You completed all steps to deploy {s1} extractor. Your {s2} extractor is now running in "
        "production.",
        "green",
    )


def get_tenant_names_extractor_workflow(ui) -> Dict:
    """
    Asks the user to choose the naming convention of the tenants for the extractor workflow:
    Option 1): <project>-dev, <project>-test, <project>-prod
    Option 2): <project>-dev, <project>-test, <project>
    and returns the chosen option as a dictionary

    Parameters:
        ui (UserInterface):
    """
    base_tenant = prompt_for_base_info()
    dev_tenant = f"{base_tenant}-{Env.DEV}"
    test_tenant = f"{base_tenant}-{Env.TEST}"
    prod_tenant_0 = f"{base_tenant}-{Env.PROD}"
    prod_tenant_1 = f"{base_tenant}"
    tenant_names_option_0 = f"dev: {dev_tenant}, test: {test_tenant}, prod: {prod_tenant_0}"
    tenant_names_option_1 = f"dev: {dev_tenant}, test: {test_tenant}, prod: {prod_tenant_1}"
    tenant_names_option_custom = "Custom tenant names"
    tenant_names_choice = ui.choose_option(
        prompt="Which naming convention do your CDF tenants follow",
        options=[tenant_names_option_0, tenant_names_option_1, tenant_names_option_custom],
    )
    if tenant_names_choice == tenant_names_option_custom:
        dev_tenant = click.prompt("CDF development tenant name")
        test_tenant = click.prompt("CDF test tenant name")
        prod_tenant = click.prompt("CDF production tenant name")
    elif tenant_names_choice == tenant_names_option_0:
        prod_tenant = prod_tenant_0
    elif tenant_names_choice == tenant_names_option_1:
        prod_tenant = prod_tenant_1
    return {Env.BASE: base_tenant, Env.DEV: dev_tenant, Env.TEST: test_tenant, Env.PROD: prod_tenant}


def prompt_for_base_info() -> str:
    """
    Asks for the base name of the tenant
    """
    tenant = click.prompt("Name of your project / customer")

    return tenant


def get_tenant_names_data_replication() -> Dict:
    """
    Requests source and destination tenant names for the custom data replication workflow and returns both together in
    a dictionary
    """
    src_tenant = click.prompt("Name of the source tenant")
    dst_tenant = click.prompt("Name of the destination tenant")
    tenant_names = {Env.SRC: src_tenant, Env.DST: dst_tenant}
    return tenant_names


def get_tenant_info(
    secret_manager_client: SecretManagerServiceClient, tenant_names: Dict, ui: UserInterface
) -> Optional[Dict[Env, CDFInfo]]:
    """
    Collects api-key and client information about all three CDF tenants and returns them as a Dictionary

    Parameters:
        secret_manager_client (SecretManagerServiceClient):
        tenant_names (Dict): the CDF tenant names for the data replication
        ui (UserInterface):
    """
    cdf_info_dict = {}

    for env, tenant_name in tenant_names.items():
        while True:
            api_key = get_cdf_api_key(client=secret_manager_client, tenant=tenant_name, ui=ui)
            if not api_key:
                return None
            cognite_client = CogniteClient(api_key=api_key, client_name="forge-replicator", project=tenant_name)
            key_valid = is_api_key_valid(client=cognite_client, tenant=tenant_name)
            if key_valid:
                break
            else:
                cprint(
                    f'Invalid api-key for tenant "{tenant_name}". Either there exists no such CDF tenant or the '
                    f"stored api-key is not valid.",
                    "red",
                )
                alt_1 = "Enter tenant names again"
                alt_2 = f'Update api-key for tenant "{tenant_name}" in GCP'
                choice = ui.choose_option("Please choose", options=[alt_1, alt_2])
                if choice == alt_1:
                    return None
                if choice == alt_2:
                    upload_api_key_to_gcp(client=secret_manager_client, tenant=tenant_name, update=True)
        cdf_info_dict[env] = CDFInfo(tenant_name, api_key, cognite_client)

    return cdf_info_dict


def get_invalid_data_sets(data_sets: List[str], tenant_info: CDFInfo) -> List[str]:
    """
    Checks if a list of data sets exist in a given tenant and returns those that don't exist

    Parameters:
        data_sets (List[str]): List of external ids
        tenant_info (CDF_Info): tenant information such as name, api-key and CDF client
    """
    return list(filter(lambda ds: not does_data_set_exist(ds, tenant_info), data_sets))


def does_data_set_exist(data_set: str, tenant_info: CDFInfo) -> bool:
    """
    Checks if a single data set exists in a given tenant

    Parameters:
        data_set: external_id
        tenant_info (CDF_Info): tenant information such as name, api-key and CDF client
    """
    return tenant_info.client.data_sets.retrieve(external_id=data_set) is not None


def create_data_set(data_set: str, tenant_info: CDFInfo) -> None:
    """
    Creates a data set with the same name and external_id on a given tenant

    Parameters:
        data_set (str): Will be used for both name and external_id of the new data_ser
        tenant_info (CDF_Info): tenant information such as name, api-key and CDF client
    """
    tenant_info.client.data_sets.create(DataSet(name=data_set, external_id=data_set))
    logger.info(f"Created data set {data_set} on tenant {tenant_info.name}")


def is_api_key_valid(client: CogniteClient, tenant: str) -> bool:
    """
    Checks if an api_key is valid for a given tenant

    Parameters:
        client (CogniteClient):
        tenant (str): CDF tenant name
    """
    status = client.login.status()
    return status.logged_in and status.project == tenant


def get_cdf_api_key(client: SecretManagerServiceClient, tenant: str, ui: UserInterface) -> Optional[str]:
    """
    Reads the CDF api-key for a given tenant from the GCP Secret Manager. If no key found, asks to abort

    Parameters:
        client (SecretManagerServiceClient):
        tenant (str): CDF tenant name
        ui (UserInterface):
    """
    while True:
        project_id = GCP_PROJECT_NAME
        secret_id = tenant
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{'latest'}"
        try:
            response = client.access_secret_version(request={"name": name})
            payload = response.payload.data.decode()
            gcp_iam_grant_access(client=client, secret_id=tenant)
            return payload
        except NotFound:
            cprint(f'Could not access api-key for tenant "{tenant}" from GCP', "red")
            alt_1 = "Enter tenant names again"
            alt_2 = f'Upload api-key for tenant "{tenant}" as a secret to GCP'
            choice = ui.choose_option("Please choose", options=[alt_1, alt_2])
            if choice == alt_1:
                return None
            if choice == alt_2:
                upload_api_key_to_gcp(tenant=tenant, client=client)


def upload_api_key_to_gcp(tenant: str, client: SecretManagerServiceClient, update=False):
    """
    Requests and uploads CDF api-key as a secret to GCP with the correct access rights for the beam replication engine

    Parameters:
        tenant (str): CDF tenant name
        client (SecretManagerServiceClient):
        update (bool): whether secret is only updated or newly created
    """
    if not update:
        gcp_create_secret(client=client, secret_id=tenant)
        gcp_iam_grant_access(client=client, secret_id=tenant)
    api_key = click.prompt(
        f'Please paste the api-key for the tenant "{tenant}". Make sure that this api-key has the '
        f"necessary permissions (i.e. read / write for the desired data types and data sets)"
    )
    gcp_add_secret_version(client=client, secret_id=tenant, payload=api_key)


def get_extractor_names(location: Path) -> List[str]:
    """
    Reads and returns all folder names on a given Path. This way the available extractors can be read

    Parameters:
         location (Path): path within the project folder
    """
    directory = EW_OUTPUT_DIR / location
    extractor_names = [x.name for x in directory.iterdir() if x.is_dir()]
    if not extractor_names:
        # No extractors in this directory
        raise FileNotFoundError
    return extractor_names


def request_cdf_api_hosts() -> Dict:
    """
    Requests CDF source and destination api hosts and returns them as a dictionary
    """
    if click.confirm("Do you want to enter custom CDF api hosts? (Default: https://api.cognitedata.com)"):
        src_host = request_host("source")
        dst_host = request_host("target")
        return {Env.SRC: src_host, Env.DST: dst_host}
    else:
        return {Env.SRC: DEFAULT_CDF_API_HOST, Env.DST: DEFAULT_CDF_API_HOST}


def request_host(env: str) -> str:
    """
    Requests host and checks that it matches the RegEx

    Parameters:
        env (str): to let the user know for which environment the host is requested
    """
    while True:
        host = click.prompt(f"Please enter the {env} host")
        if re.match(CDF_API_HOST_REGEX, host):
            return host
        else:
            cprint(
                f"The hosting location must be a valid CDF cluster URL (for instance {DEFAULT_CDF_API_HOST})", "yellow"
            )


def check_for_rollback(tenant: str, stage: str, update: bool, file_handler: ExtractorWorkflowFileHandler):
    """
    Asks the user to perform a rollback, in case the new or updated extractor does not work as intended

    Parameters:
        tenant(str): the name of the tenant to check whether rollback desired
        stage (str): from which stage of the workflow the function is called: 'started' or 'tested'
        update (bool): True if called within update_extractor
        file_handler (ExtractorWorkflowFileHandler):
    """
    rollback = False
    extractor_age = "updated" if update else "new"
    while not click.confirm(
        f'Finally, you need to make sure that the {extractor_age} extractor "{file_handler.extractor_id}" works as '
        f'intended. To do so check if the data set "{file_handler.extractor_id}" in "{tenant}" contains the expected '
        f"data. If you are satisfied, hit enter to continue. Otherwise you can deprecate the current "
        f'work on extractor "{file_handler.extractor_id}" by entering "N" ',
        show_default=False,
        default=True,
    ):
        if click.confirm(
            f"Are you sure you want to deprecate the current work on {file_handler.extractor_id} and rollback to the "
            f"previous stage? "
        ):
            rollback = True
            file_handler.deactivate_replication(
                src_env=Env.PROD, dst_env=Env.DEV, move_from=stage, move_to="deprecated"
            )
            if update:
                file_handler.move_folder_locally(
                    src_env=Env.PROD, dst_env=Env.TEST, move_from=stage, move_to="deployed"
                )
                file_handler.move_folder_on_gcp(src_env=Env.PROD, dst_env=Env.TEST, move_from=stage, move_to="deployed")
                if stage == "tested":
                    # Reactivate replication
                    file_handler.activate_replication(src_env=Env.PROD, dst_env=Env.TEST, stage="deployed")
                    pass

            cprint(
                f'Successfully deprecated work on extractor "{file_handler.extractor_id}" and rolled back to previous '
                f"stage",
                "green",
            )
            cprint(f'Make sure to disable the {extractor_age} extractor towards "{tenant}".', "yellow")
            click.confirm("Hit enter to confirm", show_default=False)
            break

    return rollback


def does_job_id_exist(job_id: str, src_tenant: Env, dst_tenant: Env, data_type: str):
    path = CR_OUTPUT_DIR / f"{src_tenant}-{dst_tenant}" / f"{data_type}"
    if path.exists():
        existing_job_ids = [d.name for d in path.iterdir()]
        if job_id in existing_job_ids:
            return True
    return False


def gcp_create_secret(client: SecretManagerServiceClient, secret_id: str):
    """
    Create a new secret with the secret_id as name. A secret is a logical wrapper around a collection of secret
    versions. Secret versions hold the actual secret material.

    Parameters:
        client (SecretManagerServiceClient): GCP client
        secret_id (str): the name of the secret. Should be the tenant name
    """
    client.create_secret(
        request={
            "parent": f"projects/{GCP_PROJECT_NAME}",
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )


def gcp_add_secret_version(client: SecretManagerServiceClient, secret_id: str, payload):
    """
    Add a new secret version to the given secret with the provided payload, i.e. the api-key

    Parameters:
        client (SecretManagerServiceClient): GCP client
        secret_id (str): the name of the secret. Should be the tenant name
        payload (str): the CDF api-key
    """
    parent = client.secret_path(GCP_PROJECT_NAME, secret_id)
    payload = payload.encode("UTF-8")
    client.add_secret_version(request={"parent": parent, "payload": {"data": payload}})


def gcp_iam_grant_access(client: SecretManagerServiceClient, secret_id: str, members: List[str] = GS_SERVICE_ACCOUNTS):
    """
    Grant correct access rights for the beam replication engine

    Parameters:
        client (SecretManagerServiceClient): GCP client
        secret_id (str): the name of the secret. Should be the tenant name
        members (List[str]): List of service accounts
    """
    name = client.secret_path(GCP_PROJECT_NAME, secret_id)
    policy = client.get_iam_policy(request={"resource": name})
    policy.bindings.add(role="roles/secretmanager.secretAccessor", members=members)
    client.set_iam_policy(request={"resource": name, "policy": policy})


def handle_default_credentials_error(e: DefaultCredentialsError) -> NoReturn:
    """
    Handles case when GCP Authentication fails due do DefaultCredentialsError. Prints error information and exits.

    Parameters:
        e (DefaultCredentialsError)
    """
    cprint("Couldn't read GCP credentials", "red")
    cprint(f'To learn how to set up authentication, please check the "Configuration" section under {DOC_URL}', "red")
    print_goodbye()
    sys.exit(0)
