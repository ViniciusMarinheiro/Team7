import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient

"""
**** Chamadas ****
GetRating: 
    http://localhost:7071/api/func-get-rating?id=a72eb8e1-2ff2-49fd-8212-779a53c8acba
    https://func-get-rating.azurewebsites.net/api/func-get-rating?code=p-_h82qIhFoG1sC2zI6-PcptIHhkQjA87wnnWPpY7jy8AzFu0Kj09A==?id=a72eb8e1-2ff2-49fd-8212-779a53c8acba
"""

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('main...')

    try:
        id = req.params.get('id')
    except ValueError:
        return func.HttpResponse(
             "Invalid call",
             status_code=400)

    logging.info('KEY...')
    KEY = '3bGBHLiTXIXkPNnPEB5CefaguvDHQYnmYkPw2wt56RXJTNZeEXeOfpBGXOVgt86ewgKglbWNsa6fXF4mFegSwA=='
    URL = 'https://cosmos-bfyoc.documents.azure.com:443/'
    client = CosmosClient(URL, credential=KEY)
    DATABASE_NAME = 'database-bfyoc'
    database = client.get_database_client(DATABASE_NAME)
    CONTAINER_NAME = 'rating'
    container = database.get_container_client(CONTAINER_NAME)
    response = get_rating(container, id)
    return func.HttpResponse(response, status_code=200)


def get_rating(container, id):
    logging.info('get_rating...')
    sql = f"SELECT * FROM rating r WHERE r.id = '{id}'"
    items = []
    for item in container.query_items(
            query=sql,
            enable_cross_partition_query=True):
        items.append(item)    
    response = json.dumps(items, indent=True)
    logging.info(response)
    return response
