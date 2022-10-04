from peewee import *
from common.translate import Translator
from .base_model import BaseModel


class Article(BaseModel):
    id = IntegerField(primary_key=True)
    body = CharField()
    publish_date = CharField(max_length=20)
    title = CharField(max_length=50)
    url = CharField(max_length=100)
    author = CharField(max_length=30)
    keyword = CharField(max_length=30)
    attachment = CharField(max_length=100)

    class Meta:
        # 表名
        table_name = 'Article'
