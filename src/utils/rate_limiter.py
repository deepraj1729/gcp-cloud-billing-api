from fastapi import HTTPException, status
from datetime import datetime, timedelta
from fastapi.routing import Request
from cachetools import LRUCache
from src.utils import constants
from logging import getLogger

logger = getLogger(__name__)

rate_limit_cache = LRUCache(maxsize=constants.LRU_CACHE_MAX_SIZE)

def rate_limiter(request: Request):
    client_ip = request.client.host

    #? Get or create a per-client IP rate limit tracker
    tracker = rate_limit_cache.setdefault(client_ip, {"requests": 0, "last_reset": datetime.utcnow()})

    #? Check if the rate limit is exceeded
    now = datetime.utcnow()
    time_since_last_reset = now - tracker["last_reset"]

    logger.info(f"IP: {client_ip}")
    logger.info(f"Request count: {tracker['requests']}")
    logger.info(f"Time since last reset: {time_since_last_reset}")

    if time_since_last_reset > timedelta(seconds=constants.LRU_CACHE_RETENTION_PERIOD):
        #* Reset the rate limit tracker if retention period has passed since the last reset
        tracker["requests"] = 0
        tracker["last_reset"] = now

    if tracker["requests"] >= constants.MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Too many requests!!!",
        )

    #? Increment the request count
    tracker["requests"] += 1
    return request