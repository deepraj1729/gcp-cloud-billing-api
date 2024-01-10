from fastapi import HTTPException,status
from redis import ConnectionPool,StrictRedis
from src.utils import constants
from logging import getLogger

logger = getLogger(__name__)
redis_pool = None

async def initialize_redis_pool():
    try:
        logger.info("Initializing Redis Connection pool!")
        global redis_pool
        redis_pool = ConnectionPool(max_connections=100).from_url(
                url=constants.CLOUD_BILLING_REDIS_URL,decode_responses=True
        )
        logger.info("Redis connection pool initialized successfully!")
    except Exception as e:
        logger.exception(e)
        raise Exception("Unable to initialize Redis client!")

async def disconnect_redis_pool():
    try:
        logger.info("Disconnecting Redis client!")
        if redis_pool is not None:
            redis_pool.disconnect()
    
    except Exception as e:
        logger.exception(e)

def get_redis_client():
    try:
        redis_client = StrictRedis(connection_pool=redis_pool)
        return redis_client
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Unable to get Redis client!")
    finally:
        pass