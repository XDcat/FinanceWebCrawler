from peewee import Model
import config


class BaseModel(Model):
    """ 基类 """
    class Meta:
        database = config.db
