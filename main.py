import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres:postgres@localhost:5432/Python_DB_ORM'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


publisher_name = input('Ведите имя или идентификатор издателя:')

query = session.query(Stock, Book.title, Shop.name, Sale.price, Sale.date_sale)
query = query.join(Sale)
query = query.join(Shop)
query = query.join(Book)
query = query.join(Publisher)

if publisher_name.isnumeric():
    records = query.filter(Publisher.id == publisher_name)
    for r in records:
        print(*r[1:])
else:
    records = query.filter(Publisher.name == publisher_name)
    for r in records:
        print(*r[1:])

session.close()