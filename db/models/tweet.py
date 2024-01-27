from pydantic import BaseModel

class Tweet(BaseModel):
    titulo: str
    contenido: str
    link: str
