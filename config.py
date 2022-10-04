import peewee
import os

db_path = os.path.join(os.path.dirname(__file__), "database/test.db")

db = peewee.SqliteDatabase(db_path)
