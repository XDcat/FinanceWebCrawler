from peewee import *
from common.translate import Translator
from .base_model import BaseModel
from bs4 import BeautifulSoup
from config import appid, password


class Article(BaseModel):
    aid = IntegerField(primary_key=True)
    website = CharField(max_length=10)
    kind = CharField(max_length=20)
    body = CharField(null=True)
    cn_body = CharField(null=True)
    cn_title = CharField(null=True, max_length=100)
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
        body_html = BeautifulSoup(self.body, "html.parser")
        return Translator.translate(body_html.text, appid=appid, key=password)

    def display(self):
        """
        展示所有信息
        :return:
        """
        name = ["aid", 'website', 'kind', 'publish_date', 'title', 'url', 'author', 'keyword', 'attachment', 'body',
                "cn_body", "cn_title"]
        inform = [self.aid, self.website, self.kind, self.publish_date, self.title, self.url, self.author, self.keyword,
                  self.attachment, self.body, self.cn_body, self.cn_title]
        return dict(zip(name, inform))

    def __str__(self):
        res = str(self.display())
        return res
