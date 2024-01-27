from typing import List
from pydantic import BaseModel

class ResultadoBusqueda(BaseModel):
    busqueda: str
    tweets: List[dict]

