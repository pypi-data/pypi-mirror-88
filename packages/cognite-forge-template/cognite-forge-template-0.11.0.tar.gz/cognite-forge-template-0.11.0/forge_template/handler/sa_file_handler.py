import logging
import time
from enum import Enum
from pathlib import Path
from typing import Dict, List

from google.cloud import storage

from forge_template.config_generator import ConfigGenerator, FileType
from forge_template.paths import (
    CR_GCP_CONFIG_PATH,
    CR_GCP_SCHEDULE_PATH,
    CR_OUTPUT_DIR,
    CR_SCHEDULE_TEMPLATE,
    EW_GCP_CONFIG_PATH,
    EW_GCP_SCHEDULE_PATH,
    EW_OUTPUT_DIR,
    EW_SCHEDULE_TEMPLATE,
    JOB_CONFIG_SCHEMA_PATH,
    JOB_CONFIG_TEMPLATE,
)
from forge_template.sa_constants import (
    COMPOSER_BUCKET,
    DATA_TYPE_OPTIONS,
    GCP_PROJECT_NAME,
    JOB_CONFIGS_BUCKET,
    JOB_DEFINITIONS_BUCKET,
)
from forge_template.util.file_util import load_yaml, move_directory, save_toml
from forge_template.util.jinja2_util import render
from forge_template.util.sa_util import get_utc_timestamp_as_str

logger = logging.getLogger(__file__)


class Env(Enum):
    BASE = "base"
    DEV = "dev"
    TEST = "test"
    PROD = "prod"
    SRC = "src"
    DST = "dst"

    def __str__(self):
        return self.value


class FileHandler:
    def __init__(self) -> None:
        self.gcp_client = storage.Client()

    def upload_blob(self, bucket_name: str, source_file_name: str, destination_blob_name: Path) -> None:
        """
        Uploads a file to the gcp bucket.

        Parameters:
            bucket_name (str): GCP bucket name
            source_file_name (str): local path to file
            destination_blob_name (Path): destination path
        """
        bucket = self.gcp_client.bucket(bucket_name)
        blob = bucket.blob(str(destination_blob_name))

        blob.upload_from_filename(source_file_name)

    def delete_blob(self, bucket_name: str, blob_name: str) -> None:
        """
        Deletes a folder from the gcp bucket.

        Parameters:
            bucket_name (str): GCP bucket name
            blob_name (str): path of object to be deleted
        """
        bucket = self.gcp_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()

    def copy_blob(
        self, bucket_name: str, blob_name: str, destination_bucket_name: str, destination_blob_name: Path
    ) -> None:
        """
        Copies a blob from one bucket to another with a new name.

        Parameters:
            bucket_name (str): GCP bucket name (source)
            blob_name (str): object path (source)
            destination_bucket_name (str): GCP bucket name (destination)
            destination_blob_name (Path): object path (target)
        """
        source_bucket = self.gcp_client.bucket(bucket_name)
        source_blob = source_bucket.blob(blob_name)
        destination_bucket = self.gcp_client.bucket(destination_bucket_name)

        source_bucket.copy_blob(source_blob, destination_bucket, str(destination_blob_name))

    def list_blobs_with_prefix(self, bucket_name: str, prefix: Path) -> List[str]:
        """
        Lists all the blobs in the bucket that begin with the prefix.

        Parameters:
            bucket_name (str): GCP bucket name (source)
            prefix (Path): prefix of path to object
        """
        return [blob.name for blob in self.gcp_client.list_blobs(bucket_name, prefix=str(prefix))]


class ExtractorWorkflowFileHandler(FileHandler):
    def __init__(self, base_tenant: str, extractor_id: str, schedule: str = "") -> None:
        super().__init__()
        self.base_tenant = base_tenant
        self.extractor_id = extractor_id
        self.schedule = schedule

        self.config_files_path = Path()

    def generate_config_files(self, data_sets_to_replicate: List[str], src_env: Env, dst_env: Env, stage: str) -> None:
        """
        Generates all 6 config files: jobs and schedules for assets, time series and events.

        Parameters:
            data_sets_to_replicate (List[str]): list of external ids
            src_env (Env): The environment of the data replication source.
            dst_env (Env): The environment of the data replication destination.
            stage (str): in which stage the config files are generated.
        """
        dst_path = EW_OUTPUT_DIR / self.base_tenant / f"{src_env}-{dst_env}" / stage / self.extractor_id
        dst_path.mkdir(parents=True, exist_ok=True)
        self.config_files_path = dst_path

        self.generate_job_config_files(dst_path, data_sets_to_replicate)
        self.generate_schedule_config_files(path=dst_path, src_env=src_env, dst_env=dst_env)

    @staticmethod
    def generate_job_config_files(path: Path, data_sets_to_replicate: List[str]) -> None:
        """
        Generates asset, time series and events config file and stores them under path

        Parameters:
            path (Path): destination path of the config files
            data_sets_to_replicate (List[str]): list of external ids
        """
        config_dict = load_yaml(JOB_CONFIG_TEMPLATE)

        for job in DATA_TYPE_OPTIONS:
            job_config_dict = config_dict[job]
            job_config_dict["allowList"]["dataSetExternalId"] = data_sets_to_replicate
            full_path = path / f"{job}-config.toml"
            save_toml(full_path, job_config_dict)

    def generate_schedule_config_files(self, path: Path, src_env: Env, dst_env: Env) -> None:
        """
        Generation of schedule files

        Parameters:
            path (Path): destination path of schedule files
            src_env (str): The environment of the data replication source.
            dst_env (str): The environment of the data replication destination.
        """
        for job in DATA_TYPE_OPTIONS:
            content = {
                "job": job,
                "src_env": src_env.value,
                "dst_env": dst_env.value,
                "gcp_project_name": GCP_PROJECT_NAME,
                "job_definitions_bucket": JOB_DEFINITIONS_BUCKET,
                "job_configs_bucket": JOB_CONFIGS_BUCKET,
                "tenant": self.base_tenant,
                "extractor_id": self.extractor_id,
                "schedule": self.schedule,
                "dag_name": f"replicate_{job}_on_{self.base_tenant}_{src_env}_{dst_env}_{self.extractor_id}_"
                f"{time.strftime('%y%m%d%H%M%S', time.gmtime())}",
            }
            output_path = path / f"{job}-schedule.py"
            render(content, EW_SCHEDULE_TEMPLATE, output_path)

    def activate_replication(self, src_env: Env, dst_env: Env, stage: str) -> None:
        """
        Activates the replication by uploading the corresponding config files to gcp

        Parameters:
            src_env (Env): The environment of the data replication source.
            dst_env (Env): The environment of the data replication destination.
            stage (str): in which stage the config files are generated / the folder name of the config files
        """
        # avoid temporary and hidden files
        config_files = [f for f in self.config_files_path.iterdir() if f.is_file() and not f.name.startswith(".")]

        path_suffix = Path(self.base_tenant) / f"{src_env}-{dst_env}" / stage / self.extractor_id
        gcp_config_path = EW_GCP_CONFIG_PATH / path_suffix
        gcp_schedule_path = EW_GCP_SCHEDULE_PATH / path_suffix
        for f in config_files:
            # Upload job configs and schedules
            self.upload_blob(
                bucket_name=JOB_CONFIGS_BUCKET, source_file_name=str(f), destination_blob_name=gcp_config_path / f.name,
            )
            # Upload only schedules to COMPOSER_BUCKET
            if "schedule" in f.name:
                self.upload_blob(
                    bucket_name=COMPOSER_BUCKET,
                    source_file_name=str(f),
                    destination_blob_name=gcp_schedule_path / f.name,
                )

    def deactivate_replication(self, src_env: Env, dst_env: Env, move_from: str, move_to: str) -> None:
        """
        Deactivates the replication by deleting the schedule files from COMPOSER_BUCKET and updating the folder
        structure locally and on JOB_CONFIGS_BUCKET

        Parameters:
            src_env (Env): The environment of the data replication source.
            dst_env (Env): The environment of the data replication destination.
            move_from (str): Current location of the config files of the replication to be deactivated
            move_to (str): New location after replication has been deactivated.
        """
        timestamp = ""
        if move_to in ["deactivated", "deprecated"]:
            timestamp = get_utc_timestamp_as_str()
        self.delete_schedule_files(src_env=src_env, dst_env=dst_env, stage=move_from)
        self.move_folder_locally(
            src_env=src_env, dst_env=dst_env, move_from=move_from, move_to=move_to, timestamp=timestamp
        )
        self.move_folder_on_gcp(
            src_env=src_env, dst_env=dst_env, move_from=move_from, move_to=move_to, timestamp=timestamp
        )

    def delete_schedule_files(self, src_env: Env, dst_env: Env, stage: str) -> None:
        """
        Deletes schedule files in COMPOSER_BUCKET/dags

        Parameters:
            src_env (str): The environment of the data replication source.
            dst_env (str): The environment of the data replication destination.
            stage (str): The stage in which the files are before deletion, i.e. "started" or "tested"
        """
        path = EW_GCP_SCHEDULE_PATH / self.base_tenant / f"{src_env}-{dst_env}" / stage / self.extractor_id
        files_to_delete = self.list_blobs_with_prefix(COMPOSER_BUCKET, prefix=path)
        for f in files_to_delete:
            self.delete_blob(bucket_name=COMPOSER_BUCKET, blob_name=f)

    def move_folder_locally(
        self, src_env: Env, dst_env: Env, move_from: str, move_to: str, timestamp: str = ""
    ) -> None:
        """
        Moves a folder locally

        Parameters:
            src_env (Env): The environment of the data replication source.
            dst_env (Env): The environment of the data replication destination.
            move_from (str): Current location of the config files of the replication to be moved
            move_to (str): New location after replication has been moved.
            timestamp (str): timestamp to be added to folder name. If empty, no timestamp is added
        """
        base_path = Path(EW_OUTPUT_DIR) / self.base_tenant / f"{src_env}-{dst_env}"
        src_path = base_path / move_from / self.extractor_id if move_from else base_path / self.extractor_id
        folder_name = f"{self.extractor_id}_{timestamp}" if timestamp else self.extractor_id
        dst_path = base_path / move_to / folder_name
        move_directory(src=src_path, dst=dst_path)

        self.config_files_path = dst_path

    def move_folder_on_gcp(self, src_env: Env, dst_env: Env, move_from: str, move_to: str, timestamp: str = "") -> None:
        """
        Moves a folder in the GCP project to deactivated or started

        Parameters:
            src_env (Env): The environment of the data replication source.
            dst_env (Env): The environment of the data replication destination.
            move_from (str): Current location of the config files of the replication to be moved
            move_to (str): New location after replication has been moved.
            timestamp (str): timestamp to be added to folder name. If empty, no timestamp is added
        """
        folder_name = f"{self.extractor_id}_{timestamp}" if timestamp else self.extractor_id

        # 1) Move on config bucket
        base_config_path = EW_GCP_CONFIG_PATH / self.base_tenant / f"{src_env}-{dst_env}"
        old_config_path = (
            base_config_path / move_from / self.extractor_id if move_from else base_config_path / self.extractor_id
        )
        new_config_path = base_config_path / move_to / folder_name
        config_files_to_move = self.list_blobs_with_prefix(JOB_CONFIGS_BUCKET, prefix=old_config_path)
        for f in config_files_to_move:
            self.copy_blob(
                bucket_name=JOB_CONFIGS_BUCKET,
                blob_name=f,
                destination_bucket_name=JOB_CONFIGS_BUCKET,
                destination_blob_name=new_config_path / Path(f).name,
            )
            self.delete_blob(bucket_name=JOB_CONFIGS_BUCKET, blob_name=f)

        # 2) Move on schedule bucket
        base_schedule_path = EW_GCP_SCHEDULE_PATH / self.base_tenant / f"{src_env}-{dst_env}"
        old_schedule_path = (
            base_schedule_path / move_from / self.extractor_id if move_from else base_schedule_path / self.extractor_id
        )
        new_schedule_path = base_schedule_path / move_to / folder_name
        schedule_files_to_move = self.list_blobs_with_prefix(COMPOSER_BUCKET, prefix=old_schedule_path)
        for f in schedule_files_to_move:
            self.copy_blob(
                bucket_name=COMPOSER_BUCKET,
                blob_name=f,
                destination_bucket_name=COMPOSER_BUCKET,
                destination_blob_name=new_schedule_path / Path(f).name,
            )
            self.delete_blob(bucket_name=COMPOSER_BUCKET, blob_name=f)


class CustomReplicatorFileHandler(FileHandler):
    def __init__(self, data_type: str, schedule: str, tenant_names: Dict, cdf_api_hosts: Dict, job_id: str) -> None:
        super().__init__()
        self.data_type = data_type
        self.schedule = schedule
        self.src_tenant = tenant_names[Env.SRC]
        self.dst_tenant = tenant_names[Env.DST]
        self.src_host = cdf_api_hosts[Env.SRC]
        self.dst_host = cdf_api_hosts[Env.DST]

        self.base_path = Path(f"{self.src_tenant}-{self.dst_tenant}", f"{data_type}", f"{job_id}")

        self.local_base_path = CR_OUTPUT_DIR / self.base_path
        self.local_job_config_path = self.local_base_path / f"{job_id}.toml"
        self.local_schedule_path = self.local_base_path / f"{job_id}-schedule.py"
        self.local_base_path.mkdir(exist_ok=True, parents=True)

        self.config_generator = ConfigGenerator(FileType.TOML)

    def generate_job_config(self) -> None:
        """
        Generates, validates and saves the config file for the data replication based on the user's input
        """
        self.config_generator.set_schema_info(
            output_path=self.local_job_config_path,
            schema_path=JOB_CONFIG_SCHEMA_PATH,
            key=self.data_type,
            post_transforms=[],
        )
        self.config_generator.generate()

        self.fix_config_keys()

    def generate_schedule(self) -> None:
        """
        Generates and saves the schedule file for the data replication based on the user specified schedule
        """
        content = {
            "data_type": self.data_type,
            "src_tenant": self.src_tenant,
            "dst_tenant": self.dst_tenant,
            "src_host": self.src_host,
            "dst_host": self.dst_host,
            "schedule": self.schedule,
            "path": self.base_path,
            "job_config_name": self.local_job_config_path.name,
            "dag_name": f"replicate_{self.data_type}_from_{self.src_tenant}_to_{self.dst_tenant}_"
            f"{time.strftime('%y%m%d%H%M%S', time.gmtime())}",
            "gcp_project_name": GCP_PROJECT_NAME,
            "job_definitions_bucket": JOB_DEFINITIONS_BUCKET,
            "job_configs_bucket": JOB_CONFIGS_BUCKET,
        }
        render(content, CR_SCHEDULE_TEMPLATE, self.local_schedule_path)

    def upload_configs_to_gcp(self) -> None:
        """
        Activates the replication by uploading config and schedule files to GCP
        """
        self.upload_blob(
            bucket_name=JOB_CONFIGS_BUCKET,
            source_file_name=str(self.local_job_config_path),
            destination_blob_name=CR_GCP_CONFIG_PATH / self.base_path / self.local_job_config_path.name,
        )
        self.upload_blob(
            bucket_name=JOB_CONFIGS_BUCKET,
            source_file_name=str(self.local_schedule_path),
            destination_blob_name=CR_GCP_CONFIG_PATH / self.base_path / self.local_schedule_path.name,
        )
        self.upload_blob(
            bucket_name=COMPOSER_BUCKET,
            source_file_name=str(self.local_schedule_path),
            destination_blob_name=CR_GCP_SCHEDULE_PATH / self.base_path / self.local_schedule_path.name,
        )

    def fix_config_keys(self) -> None:
        """
        The config generator generates config files with keys like "[assets.config]". The beam replicator can only
        handle keys of the form "[config]". This function fixes the config files to be processable by
        the beam-replicator.
        """
        self.config_generator.config = self.config_generator.config[self.data_type]
