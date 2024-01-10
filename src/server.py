from src.utils.billing import initialize_billing_client
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.utils.redis import initialize_redis_pool
from src.utils.rate_limiter import rate_limiter
from src.models.healthcheck import HealthCheck
from src.routes.billing import billing_router
from src.routes.alert import alerting_router
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Google Cloud Billing",
    description="Cloud Billing - Cost monitoring and Alerting for Google Cloud Platform",
    version="1.0.0"
)

#? Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup",initialize_billing_client)
app.add_event_handler("startup",initialize_redis_pool)

@app.exception_handler(HTTPException)
async def http_exception_handler(request,exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get(path="/health",response_model=HealthCheck,status_code=200,tags=["HealthCheck"],dependencies=[Depends(rate_limiter)])
async def health_check():
    return HealthCheck(status="OK")

app.include_router(router=billing_router,tags=['Billing'],dependencies=[Depends(rate_limiter)])
app.include_router(router=alerting_router,tags=['Alerts'],dependencies=[Depends(rate_limiter)])