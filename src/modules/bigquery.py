from google.cloud import bigquery
from google.cloud.bigquery.job import QueryJob

class BigQueryClient:
    def __init__(self,project_id:str) -> None :
        self.project_id = project_id
        self.client = bigquery.Client(project=self.project_id)
    
    def query(self,sql_query:str) -> QueryJob:
        return self.client.query(query=sql_query)