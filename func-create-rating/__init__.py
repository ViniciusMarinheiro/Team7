import json
import logging
import uuid
from datetime import datetime
import azure.functions as func
from azure.cosmos import CosmosClient

"""
**** Chamadas ****
Create: 
    http://localhost:7071/api/func-create-rating => Passar body
"""

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('main...')

    try:
        payload = req.get_json()
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
    response = create_rating(container, payload)
    return func.HttpResponse(response, status_code=200)


def create_rating(container, payload):
    logging.info('create_rating...')    
    logging.info(payload)
    id = uuid.uuid4()
    data = {
        "id": str(id) ,
        "userId": payload["userId"],
        "productId": payload["productId"],
        "timestamp":datetime.utcnow().isoformat() + 'Z',
        "locationName": payload["locationName"],
        "rating": payload["rating"],
        "userNotes": payload["userNotes"]
    }
    logging.info(data)
    container.upsert_item(data)
    response = json.dumps(data, indent=True)
    return response
