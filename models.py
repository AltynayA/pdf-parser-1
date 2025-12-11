from pydantic import BaseModel,field_validator


class PropertyInput(BaseModel):
    title: str
    city: str
    price: float 
    area_sqm: float 
    bedrooms: int
    year_built: int 
    is_furnished: bool = False

    @field_validator('price', 'area_sqm',"bedrooms", "year_built", mode="before")
    def greater_than_zero(cls, v):
        if v <= 0:
            raise ValueError('Must be greater than zero')
        return v