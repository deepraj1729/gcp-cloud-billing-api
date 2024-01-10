from fastapi import HTTPException,status
from src.modules.billing import CloudBilling
from src.utils import constants
from logging import getLogger

logger = getLogger(__name__)
billing_client = None

async def initialize_billing_client():
    try:
        logger.info("Initializing Cloud billing client!")
        global billing_client
        billing_client = CloudBilling(
            project_id=constants.CLOUD_BILLING_EXPORT_PROJECT_ID,
            dataset_id=constants.CLOUD_BILLING_EXPORT_DATASET_ID,
            table_id=constants.CLOUD_BILLING_EXPORT_TABLE_ID
        )
        logger.info("Cloud billing client initialized successfully!")

    except Exception as e:
        logger.exception(e)
        raise Exception("Unable to initialize billing client!")

def get_cloud_billing_client():
    try:
        if billing_client is None:
           raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Unable to get billing client!")
        return billing_client
    except Exception as e:
        logger.exception(e)
    finally:
        pass