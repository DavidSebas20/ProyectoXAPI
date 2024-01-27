from fastapi import APIRouter
import requests
from db.models.tweet import Tweet
from db.client import db_client
from fastapi import status

router=APIRouter(prefix="/tweets",tags=["tweets"],responses={404:{"message":"No encontrado"}})

#Buscador de Tweets
@router.get("/",status_code=status.HTTP_201_CREATED)
async def tweets(numero: int, busqueda: str):
    
    twitter_data = []
    
    payload = {
        'api_key': '321700ac46a41ee97ced9b318a8201fb',
        'query': busqueda,
        'num': numero
    }

    response = requests.get('https://api.scraperapi.com/structured/twitter/search', params=payload)
    data = response.json()
    tweets = data['organic_results']

    for tweet in tweets:
        twitter_data.append(Tweet(
            titulo=tweet.get("title", ""),
            contenido=tweet.get("snippet", ""),
            link=tweet.get("link", "")
        ))
    
    resultados = {"busqueda": busqueda, "tweets": [tweet.dict() for tweet in twitter_data]}

    try:
        db_client.tweets.insert_one(resultados)
        return {"busqueda": busqueda, "tweets":twitter_data}
    except:
        return {"error":"No se pudo encontrar los tweets"}


#Trae todos los tweets
@router.get("/todos",status_code=status.HTTP_202_ACCEPTED)
async def todos():
    
    try:
        todos_los_tweets = list(db_client.tweets.find())
        for tweet in todos_los_tweets:
            tweet['_id'] = str(tweet['_id'])
        return todos_los_tweets
    except:
        return {"error": "No se pudieron obtener los tweets de la base de datos"}