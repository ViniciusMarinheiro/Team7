import json
import logging
import uuid
from datetime import datetime
import azure.functions as func
from azure.cosmos import CosmosClient

"""
**** Chamadas ****
Create: 
    http://localhost:7071/api/api-bfyoc-rating-team7?call=create_rating => Passar body
    https://func-team7.azurewebsites.net/api/api-bfyoc-rating-team7?code=kbC29l65GuIbN1ta64EpBDvlPH8RgjCJbLqVr6R-ehcPAzFumgtJaQ==&call=create_rating
GetRating:
    http://localhost:7071/api/api-bfyoc-rating-team7?call=rating&id=a72eb8e1-2ff2-49fd-8212-779a53c8acba
    https://func-team7.azurewebsites.net/api/api-bfyoc-rating-team7?code=kbC29l65GuIbN1ta64EpBDvlPH8RgjCJbLqVr6R-ehcPAzFumgtJaQ==&call=get_rating&id=a72eb8e1-2ff2-49fd-8212-779a53c8acba
GetRatings:
    http://localhost:7071/api/api-bfyoc-rating-team7?call=ratings
    https://func-team7.azurewebsites.net/api/api-bfyoc-rating-team7?code=kbC29l65GuIbN1ta64EpBDvlPH8RgjCJbLqVr6R-ehcPAzFumgtJaQ==&call=get_ratings
"""

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('main...')
    call = req.params.get('call')    
    if not call:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            call = req_body.get('call')

    if call:
        URL = 'https://cosmos-bfyoc.documents.azure.com:443/'
        KEY = '3bGBHLiTXIXkPNnPEB5CefaguvDHQYnmYkPw2wt56RXJTNZeEXeOfpBGXOVgt86ewgKglbWNsa6fXF4mFegSwA=='
        client = CosmosClient(URL, credential=KEY)
        DATABASE_NAME = 'database-bfyoc'
        database = client.get_database_client(DATABASE_NAME)
        CONTAINER_NAME = 'rating'
        container = database.get_container_client(CONTAINER_NAME)
        if call == 'get_ratings':
            response = get_ratings(container)
            return func.HttpResponse(response, status_code=200)
        elif call == 'get_rating':
            id = req.params.get('id')
            response = get_rating(container, id)
            return func.HttpResponse(response, status_code=200)
        elif call == 'create_rating':
            payload = req.get_json()
            response = create_rating(container, payload)
            return func.HttpResponse(response, status_code=200)
    else:
        return func.HttpResponse(
             "Invalid call",
             status_code=400
        )


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
