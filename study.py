import sqlalchemy as db
from sqlalchemy import select
import db.py
engine = db.create_engine('sqlite:///listings.db')
conn = engine.connect()
metadata = db.MetaData()


