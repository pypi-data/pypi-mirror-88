import time

from forge_template.sa_constants import GCP_PROJECT_NAME


def get_utc_timestamp_as_str(f="%y%m%d%H%M%S") -> str:
    return time.strftime(f, time.gmtime())


def print_monitor_replication():
    print(
        f"To monitor the replication job, visit: https://console.cloud.google.com/dataflow/jobs?project="
        f"{GCP_PROJECT_NAME} \n (It may take some time until the job appears)"
    )
