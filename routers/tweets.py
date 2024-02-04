from fastapi import APIRouter
from db.client import db_client
from fastapi import status
from ntscraper import Nitter
from pysentimiento import create_analyzer
import json


router=APIRouter(prefix="/tweets",tags=["tweets"],responses={404:{"message":"No encontrado"}})

scraper = Nitter(0)

analyzer = create_analyzer(task="sentiment", lang="es")


#Buscador de Tweets
@router.get("/busqueda", status_code=status.HTTP_201_CREATED)
async def tweets(busqueda: str, metodo: str, numero: int):

    twitter_data = get_tweets(busqueda, metodo, numero)

    resultados = {"busqueda": busqueda, "metodo": metodo, "tweets": twitter_data}

    try:
        with open(f'data_{busqueda}_{metodo}_{numero}.json', 'w') as json_file:
            json.dump(resultados, json_file, indent=4)
        db_client.tweets.insert_one(resultados)
        return {"busqueda": busqueda,"metodo":metodo, "tweets": twitter_data}
    except Exception as e:
        return {"error": f"No se pudo encontrar los tweets: {e}"}



#Trae todos los tweets
@router.get("/",status_code=status.HTTP_202_ACCEPTED)
async def todos():
    
    try:
        todos_los_tweets = list(db_client.tweets.find())
        for tweet in todos_los_tweets:
            tweet['_id'] = str(tweet['_id'])
        return todos_los_tweets
    except:
        return {"error": "No se pudieron obtener los tweets de la base de datos"}
 
 
#Metodo que me trae los tweets  
def get_tweets(name, modes, no):
    tweets = scraper.get_tweets(name, mode=modes, number=no)
    final_tweets = []
    for x in tweets['tweets']:
        pos = analyzer.predict(x['text']).output
        data = {
            'link': x['link'],
            'text': x['text'],
            'likes': x['stats']['likes'],
            'commentarios': x['stats']['comments'],
            'retweets': x['stats']['retweets'],
            'sentimiento': pos
        }
        final_tweets.append(data)
    return final_tweets