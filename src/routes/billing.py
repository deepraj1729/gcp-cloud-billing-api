from src.utils.billing import get_cloud_billing_client
from fastapi import Depends, HTTPException,status
from src.utils.redis import get_redis_client
from src.modules.billing import CloudBilling
from src.models.response import ResponseModel
from src.utils import constants
from fastapi import APIRouter
from logging import getLogger
from redis import StrictRedis
import json

logger = getLogger(__name__)
billing_router = APIRouter(prefix="/api/billing")

@billing_router.get(path="/cost",status_code=200,response_model=ResponseModel)
async def get_billing_cost_by_range(
    q:str,
    cloud_billing_client:CloudBilling = Depends(get_cloud_billing_client),
    redis_client:StrictRedis = Depends(get_redis_client)
):
    try:
        cache_key = f"total_cost_last_{q}"
        cache_data = redis_client.hgetall(name=cache_key)

        if cache_data != {}:
            logger.info("Cache Hit!")
            return ResponseModel(
                data=json.loads(cache_data["total_billing"]),
                message=f"Total Cloud Billing cost for time_range: {q}"
            )

        logger.info(f"Cache Miss!")
        response = await cloud_billing_client.calculate_total_cost_by_range(str_time_range=q)
        redis_client.hmset(cache_key,{"total_billing":json.dumps(response)})
        redis_client.expire(name=cache_key,time=constants.REDIS_KEY_EXPIRE_INTERVAL)
        logger.info(f"Updated Cache for key: {cache_key} and set expiry time of {constants.REDIS_KEY_EXPIRE_INTERVAL}s")

        return ResponseModel(
            data=response,
            message=f"Total Cloud Billing cost for time_range: {q}"
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid parameters passed! Exception: {e}"
        )

@billing_router.get(path="/resources",status_code=200,response_model=ResponseModel)
async def get_billing_resources_by_range(
    q:str,
    limit:int=10,
    cloud_billing_client:CloudBilling = Depends(get_cloud_billing_client),
    redis_client:StrictRedis = Depends(get_redis_client)
):
    try:
        cache_key = f"resource_cost_last_{q}_limit_{limit}"
        cache_data = redis_client.hgetall(name=cache_key)

        if cache_data != {}:
            logger.info("Cache Hit!")
            return ResponseModel(
                data=json.loads(cache_data["resource_billing"]),
                message=f"Top most costly resources for time_range: {q}"
            )

        logger.info(f"Cache Miss!")
        response = await cloud_billing_client.list_most_costly_resources_by_range(str_time_range=q,limit=limit)
        redis_client.hmset(cache_key,{"resource_billing": json.dumps(response)})
        redis_client.expire(name=cache_key,time=constants.REDIS_KEY_EXPIRE_INTERVAL)
        logger.info(f"Updated Cache for key: {cache_key} and set expiry time of {constants.REDIS_KEY_EXPIRE_INTERVAL}s")

        return ResponseModel(
            data=response,
            message=f"Top most costly resources for time_range: {q}"
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid parameters passed! Exception: {e}"
        )