from peewee import *
from common.translate import Translator
from .base_model import BaseModel


class Article(BaseModel):
    website = CharField(max_length=10)
    type = CharField(max_length=20)
    id = IntegerField(primary_key=True)
    body = CharField(null=True)
    publish_date = CharField(max_length=20, null=True)
    title = CharField(max_length=50)
    url = CharField(max_length=100)
    author = CharField(max_length=30, null=True)
    keyword = CharField(max_length=30, null=True)
    attachment = CharField(max_length=100, null=True)

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

    def display(self):
        """
        展示所有信息
        :return:
        """
        name = ["body", 'publishdata', 'title', 'url', 'author', 'keyword', 'attachment']
        inform = [self.body, self.publish_date, self.title, self.url, self.author, self.keyword, self.attachment]
        return dict(zip(name, inform))

    def __str__(self):
        res = str(self.display())
        return res

