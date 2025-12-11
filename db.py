import sqlalchemy as db
from sqlalchemy import select

engine = db.create_engine('sqlite:///listings.db')
conn = engine.connect()
metadata = db.MetaData()


listings = db.Table(
    'listings', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('title', db.Text),
    db.Column('city', db.Text),
    db.Column('price', db.Integer),
    db.Column('area_sqm', db.Float),
    db.Column('bedrooms', db.Integer),
    db.Column('bathrooms', db.Integer),
    db.Column('year_built', db.Integer),
    db.Column('is_furnished', db.Boolean, default=False) 
)

metadata.create_all(engine)

query = select(listings)

# Выполняем его
result = conn.execute(query)

# Забираем все строки
rows = result.fetchall()

# Выводим
for row in rows:
    print(row)