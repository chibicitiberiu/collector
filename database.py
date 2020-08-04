from peewee import DatabaseProxy, Model
from playhouse.db_url import connect
from playhouse.pool import PooledPostgresqlExtDatabase
import config

DB = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = DB

def initialize_db():
    db = connect(config.DATABASE_URL)
    DB.initialize(db)