from enum import Enum, unique


@unique
class ServiceNameEnum(Enum):
    SecOps = "sec-ops-web"
    CICD = "cicd"
    CMDB = "cmdb"
    CCENTER = "confcenter"
    WORKFLOWAPI = "workflow"
    OPS_WORKFLOW_ENGINE = "ops-workflow-engine"
    DB_MANAGE = "db-manage"
    NIGHT_INGALE = "nightingale"
    SISYPHE_HDFS_SERVER = "sisyphe-hdfs-server"
    AIRFLOW = "airflow-webserver"
