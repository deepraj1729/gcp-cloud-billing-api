import os

#? Environment variables
CLOUD_BILLING_EXPORT_PROJECT_ID     = os.environ["CLOUD_BILLING_EXPORT_PROJECT_ID"]     # Billing Export Project
CLOUD_BILLING_EXPORT_DATASET_ID     = os.environ["CLOUD_BILLING_EXPORT_DATASET_ID"]     # Billing Export Dataset ID
CLOUD_BILLING_EXPORT_TABLE_ID       = os.environ["CLOUD_BILLING_EXPORT_TABLE_ID"]       # Billing Export Table ID
CLOUD_BILLING_REDIS_URL             = os.environ["CLOUD_BILLING_REDIS_URL"]             # Redis URL
MAX_REQUESTS_PER_MINUTE             = int(os.environ["MAX_REQUESTS_PER_MINUTE"])        # Rate limiter
LRU_CACHE_MAX_SIZE                  = int(os.environ["LRU_CACHE_MAX_SIZE"])             # Max LRU Cache entries
LRU_CACHE_RETENTION_PERIOD          = int(os.environ["LRU_CACHE_RETENTION_PERIOD"])     # Cache Retention (seconds)
MAX_BILLING_RESOURCE_COUNT          = int(os.environ["MAX_BILLING_RESOURCE_COUNT"])     # Max rows per resource
REDIS_KEY_EXPIRE_INTERVAL           = int(os.environ["REDIS_KEY_EXPIRE_INTERVAL"])      # Redis key expiry (seconds)