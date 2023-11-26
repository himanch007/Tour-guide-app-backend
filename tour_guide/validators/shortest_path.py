from pydantic import BaseModel


class shortestPathRequestFormat(BaseModel):
    names: list
    current_coordinates: list