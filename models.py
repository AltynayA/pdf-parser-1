from pydantic import BaseModel


class PropertyInput(BaseModel):
    title: str
    city: str
    price: float 
    area_sqm: float 
    bedrooms: int
    year_built: int 
    is_furnished: bool = False