# peewee documentation: peewee.readthedocs.io/en/latest/peewee/models.html
from peewee import *

# Set Database
db = SqliteDatabase('DataBase/db/database.db')

# Set entities. Model - basic ORM model
class BaseModel(Model):
    id = PrimaryKeyField(unique = True)  # Unique Primary key

    class Meta:
        database = db
        order_by = 'id'


class Type(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'types'  # table's name


class City(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'cities'


class Source(BaseModel):
    date = DateField()
    city_id = ForeignKeyField(City)
    weather = FloatField()
    type_id = ForeignKeyField(Type)

    class Meta:
        db_table = 'sources'