import sqlalchemy as db

engine = db.create_engine('sqlite:///books.db')
conn = engine.connect()
metadata = db.MetaData()

books = db.Table(
    'books', metadata,
    db.Column('book_id', db.Integer, primary_key=True),
    db.Column('book_name', db.Text),
    db.Column('book_author', db.Text),
    db.Column('book_year', db.Integer),
    db.Column('book_is_taken', db.Boolean, default=False)
)

metadata.create_all(engine)

# нормальная вставка
insertion_query = books.insert()
conn.execute(insertion_query, [
    {'book_name': 'Бесы', 'book_author': 'Фёдор Достоевский', 'book_year': 1872},
    {'book_name': 'Старик и море', 'book_author': 'Эрнест Хемингуэй', 'book_year': 1952}
])

# удаляем лишние записи
deletion_query = books.delete().where(books.c.book_id >= 3)
conn.execute(deletion_query)
#conn.execute(books.delete().where(books.c.book_id == 2))
#conn.commit()


# никакого лишнего insert() без данных!

conn.commit()

# выборка
rows = conn.execute(db.select(books)).fetchall()
print(rows)

# выборка по автору
author_rows = conn.execute(
    db.select(books).where(books.c.book_author == 'Фёдор Достоевский')
).fetchall()
print(author_rows)

# ещё вставка
conn.execute(insertion_query, [
    {'book_name':'Униженные и оскорблённые', 'book_author':'Фёдор Достоевский', 'book_year':1861},
    {'book_name':'Братья Карамазовы', 'book_author':'Фёдор Достоевский', 'book_year':1880}
])

conn.commit()

rows = conn.execute(db.select(books)).fetchall()
print(rows)


author_rows = conn.execute(
    db.select(books).where(books.c.book_author == 'Фёдор Достоевский')
).fetchall()
print(author_rows)

update_query = books.update().where(books.c.book_id == 4).values(book_year=1875)

conn.execute(update_query)
conn.commit()

rows = conn.execute(db.select(books)).fetchall()
print(rows)

update_query = books.update().where(books.c.book_id == 1).values(book_year=1872)

conn.execute(update_query)
conn.commit()

rows = conn.execute(db.select(books)).fetchall()
print(rows)

deletion_query = books.delete().where(books.c.book_name == 'Бесы')
conn.execute(deletion_query)
conn.commit()

rows = conn.execute(db.select(books)).fetchall()
print(rows)

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
	pass

class UserBase(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(30))