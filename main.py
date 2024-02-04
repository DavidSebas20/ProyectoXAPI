from fastapi import FastAPI
from routers import tweets


app=FastAPI()

#Routers
app.include_router(tweets.router)


@app.get("/")
async def root():
    return "Arquitectura de Software" 
