from model.article import Article
from utils import ormutils

class TestArticle:
    def test_article(self):
        ormutils.create_table(Article)
        article = Article.create(
            publish_date="09 02 2022",
            body="<br>adadwa<br><p></p>", title="hello",
            url="https://www.baidu.com",
            author="me",
            keyword="yae",
            attachment="https://www.baidu.com"
        )
        article.save()
