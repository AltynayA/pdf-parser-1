
from fastapi import FastAPI, HTTPException
from models import PropertyInput
from db import conn, listings
import sqlalchemy as db

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
    return {
        "message": "JSON is valid",
        "validated_data": data.model_dump()
    }

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
        result = conn.execute(insert_query)
        conn.commit()

        inserted_id = result.inserted_primary_key[0]

        record = conn.execute(
            db.select(listings).where(listings.c.id == inserted_id)
        ).fetchone()

        return {
            "message": "JSON is valid and saved to DB ✅",
            "inserted_record": dict(record)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
