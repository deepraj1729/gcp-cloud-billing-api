from src.modules.bigquery import BigQueryClient
from src.utils.timestamp import TimeRangeUtil
from src.utils import constants
from datetime import datetime

class CloudBilling:
    def __init__(self,project_id:str,dataset_id:str,table_id:str):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.client = BigQueryClient(project_id=self.project_id)
        self.time_range_util = TimeRangeUtil()
        self.max_limit = constants.MAX_BILLING_RESOURCE_COUNT

    async def calculate_total_cost_by_range(self,str_time_range:str):
        end_time_stamp = datetime.utcnow()
        start_time_stamp = end_time_stamp - self.time_range_util.get_timedelta(str_time_range=str_time_range)

        query = f"""
            SELECT
                ROUND(SUM(cost), 2) AS total_cost
            FROM
                `{self.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE
                _PARTITIONTIME BETWEEN TIMESTAMP("{start_time_stamp}") AND TIMESTAMP("{end_time_stamp}")
        """
        query_job = self.client.query(query)
        results = query_job.result()
        
        for result in results:
            total_cost = result.total_cost
            
        return {'total_cost': total_cost }


    async def list_most_costly_resources_by_range(self,str_time_range:str,limit:int=10):
        if limit > self.max_limit:
            raise Exception(f"Max limit exceeded! max_limit is {self.max_limit}")
        
        end_time_stamp = datetime.utcnow()
        start_time_stamp = end_time_stamp - self.time_range_util.get_timedelta(str_time_range=str_time_range)
        most_costly_resources_list = []

        query = f"""
            SELECT
                project.id AS project_id,
                project.name AS project_name,
                service.id AS service_id,
                service.description AS service_description,
                sku.id AS sku_id,
                sku.description AS sku_description,
                ROUND(SUM(cost), 2) AS total_cost
            FROM
                `{self.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE
                _PARTITIONTIME BETWEEN TIMESTAMP("{start_time_stamp}") AND TIMESTAMP("{end_time_stamp}")
            GROUP BY
                project_id,project_name,service_id,service_description,sku_id,sku_description
            ORDER BY
                total_cost DESC
            LIMIT {limit}
        """

        query_job = self.client.query(query)
        results = query_job.result()
        
        for row in results:
            most_costly_resources_list.append({
                "project": {
                    "project_id": row.project_id,
                    "project_name": row.project_name,
                },
                "service": {
                    "id": row.service_id,
                    "description": row.service_description,
                },
                "sku": {
                    "id": row.sku_id,
                    "description": row.sku_description
                },
                "resource_total_cost": row.total_cost
            })
        return most_costly_resources_list