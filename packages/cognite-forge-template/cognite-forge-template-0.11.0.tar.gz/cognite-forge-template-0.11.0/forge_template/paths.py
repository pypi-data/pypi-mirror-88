from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
PACKAGE_NAME = "forge_template"

CODE_DIR = ROOT_DIR / PACKAGE_NAME
TEMPLATE_DIR = CODE_DIR / "templates"

# Schema paths
SCHEMA_DIR = CODE_DIR / "schema"
YAML_CONFIG_SCHEMA_PATH = SCHEMA_DIR / "config_schema.yaml"
YAML_SECRETS_SCHEMA_PATH = SCHEMA_DIR / "secrets_schema.yaml"
JOB_CONFIG_SCHEMA_PATH = SCHEMA_DIR / "job_config_schema.yaml"

# Config paths
YAML_CONFIG_PATH = Path("config.yaml")
YAML_SECRETS_PATH = Path("secrets.yaml")

# Databricks paths
DATABRICKS_TEMPLATE_DIR = TEMPLATE_DIR / "databricks"
DATABRICKS_OUTPUT_DIR = Path("databricks")

# Power BI paths
POWERBI_TEMPLATE_DIR = TEMPLATE_DIR / "powerbi"
POWERBI_OUTPUT_DIR = Path("powerbi")
POWERBI_BASE_DATASET_PATH = POWERBI_OUTPUT_DIR / "datasets" / "base_dataset.pbix"
POWERBI_BASE_REPORT_PATH = POWERBI_OUTPUT_DIR / "reports" / "base_report.pbix"

# SA Replication paths
# Local paths
DATA_REPLICATOR_OUTPUT_DIR = Path("data_replicator")
EW_OUTPUT_DIR = DATA_REPLICATOR_OUTPUT_DIR / "extractor_workflow"
CR_OUTPUT_DIR = DATA_REPLICATOR_OUTPUT_DIR / "custom_replicator"
DATA_REPLICATOR_TEMPLATE_DIR = TEMPLATE_DIR / "data_replicator"
JOB_CONFIG_TEMPLATE = DATA_REPLICATOR_TEMPLATE_DIR / "extractor_workflow" / "job_config_file_template.yaml"
EW_SCHEDULE_TEMPLATE = DATA_REPLICATOR_TEMPLATE_DIR / "extractor_workflow" / "schedule_config_file_template.txt"
CR_SCHEDULE_TEMPLATE = DATA_REPLICATOR_TEMPLATE_DIR / "custom_replicator" / "schedule_config_file_template.txt"
# GCP paths
EW_GCP_CONFIG_PATH = Path("extractor_workflow")
EW_GCP_SCHEDULE_PATH = Path("dags", "extractor_workflow")
CR_GCP_CONFIG_PATH = Path("custom_replicator")
CR_GCP_SCHEDULE_PATH = Path("dags", "custom_replicator")

# Github Actions paths
SCRIPT_TEMPLATE_DIR = TEMPLATE_DIR / "infra_scripts"
POWERBI_SCRIPT_PATH = SCRIPT_TEMPLATE_DIR / "deploy_powerbi.py"
DATABRICKS_SCRIPT_TEMPLATE_PATH = SCRIPT_TEMPLATE_DIR / "deploy_databricks.py"
SCRIPT_OUTPUT_DIR = Path("pipeline_scripts")

WORKFLOW_TEMPLATE_DIR = TEMPLATE_DIR / "github_workflows"
POWERBI_WORKFLOW_TEMPLATE_PATH = WORKFLOW_TEMPLATE_DIR / "deploy_powerbi.yaml"
DATABRICKS_WORKFLOW_TEMPLATE_PATH = WORKFLOW_TEMPLATE_DIR / "deploy_databricks.yaml"
WORKFLOW_OUTPUT_DIR = Path(".github") / "workflows"
