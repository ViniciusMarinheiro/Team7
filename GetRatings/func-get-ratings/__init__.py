import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient

"""
**** Chamadas ****
GetRating: 
    http://localhost:7071/api/func-get-ratings
"""

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('main...')
    logging.info('KEY...')
    KEY = '3bGBHLiTXIXkPNnPEB5CefaguvDHQYnmYkPw2wt56RXJTNZeEXeOfpBGXOVgt86ewgKglbWNsa6fXF4mFegSwA=='
    URL = 'https://cosmos-bfyoc.documents.azure.com:443/'
    client = CosmosClient(URL, credential=KEY)
    DATABASE_NAME = 'database-bfyoc'
    database = client.get_database_client(DATABASE_NAME)
    CONTAINER_NAME = 'rating'
    container = database.get_container_client(CONTAINER_NAME)
    response = get_ratings(container)
    return func.HttpResponse(response, status_code=200)


def get_ratings(container):
    logging.info('get_ratings...')
    sql = f"SELECT * FROM rating"
    items = []
    logging.info('get_ratings 1 ...')
    for item in container.query_items(
            query=sql,
            enable_cross_partition_query=True):
        items.append(item)
    logging.info('get_ratings 2 ...')
    response = json.dumps(items, indent=True)
    logging.info(response)
    return response
