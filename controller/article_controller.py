from peewee import *
from model.article import Article
class BaseModel(Model):
    """
    # 基类
    """
    class Meta:
        db_path = "../database/test.db"
        db = SqliteDatabase(db_path)
        database = db

# 表类
class Article_table(BaseModel):
    id = IntegerField(primary_key=True)
    body=CharField()
    publish_date=CharField(max_length=20)
    title=CharField(max_length=50)
    url = CharField(max_length=100)
    author = CharField(max_length=30)
    keyword = CharField(max_length=30)
    attachment = CharField(max_length=100)
    class Meta:
        # 表名
        table_name = 'ArticleInformation'

    def get_val(self,article):
        """
        从article结构体获取数据
        :param article: 结构体
        :return:
        """
        self.body=article.body
        self.publish_date=article.publish_date
        self.title=article.title
        self.url=article.url
        self.author=article.author
        self.keyword=article.keyword
        self.attachment=article.attachment

# 创建表
def create_table(table):
    if not table.table_exists():
        table.create_table()

# 删除表
def drop_table(table):
    if table.table_exists():
        table.drop_table()


if __name__=='__main__':
    # test为数据库名，建立Sqlite数据库

    # 创建一张Test表
    create_table(Article_table)
    art=Article("09 02 2022","<br>adadwa<br><p></p>","hello","https://www.baidu.com","me","yae","https://www.baidu.com")
    art1=Article("09 02 2022","<br>adadada<br><p></p>","hello","https://www.wwom","ffad","we","https://www.baidu.com")

    art_table=Article_table()
    art_table.get_val(art)
    art_table.save()
