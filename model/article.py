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

    @property
    def ch_text(self):
        """
        property属性构造
        :param html_code: 正文部分的html源码
        :param appid: 翻译API账号
        :param key: 翻译API密码
        :return: 中文文本
        """
        return Translator.translate(self.body, appid='20220914001342952', key='Q_SNAXetAkmZq2yaV4o_')
