
from fastapi import FastAPI, HTTPException
from models import PropertyInput
from db import conn, listings
import sqlalchemy as db
from pydantic import field_validator

# importing Pydantic model
from models import PropertyInput
app = FastAPI()
# endpoint accepting input 

# health check 
@app.get("/")
async def root():
    return {"status": "API running"}

# validating json input
@app.post("/validate")
async def validate_property(data: PropertyInput):
    if greater_than_zero('price',"area_sqm", "bedrooms", "year_built", data):
        return {
            "message": "JSON is valid",
            "validated_data": data.model_dump()
                }
    else:
        raise HTTPException(status_code=400, detail="Validation failed")

@field_validator('price', 'area_sqm',"bedrooms", "year_built", mode="before")
def greater_than_zero(cls, v):
    if v <= 0:
        raise ValueError('Must be greater than zero')
    return v

# validating and saving to DB``
@app.post("/validate-and-save")
async def validate_and_save(data: PropertyInput):
    try:
        insert_query = listings.insert().values(
            title=data.title,
            city=data.city,
            price=data.price,
            area_sqm=data.area_sqm,
            bedrooms=data.bedrooms,
            year_built=data.year_built,
            is_furnished=data.is_furnished
        )

        greater_than_zero('price',"area_sqm", "bedrooms", "year_built", data)

        result = conn.execute(insert_query)
        conn.commit()

        inserted_id = result.inserted_primary_key[0]

        record = conn.execute(
            db.select(listings).where(listings.c.id == inserted_id)
        ).fetchone()

        return {
            "message": "JSON is valid and saved to DB ✅",
            "inserted_record": dict(record._mapping)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
