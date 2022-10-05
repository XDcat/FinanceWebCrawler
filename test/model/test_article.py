from model.article import Article
from utils import ormutils

from common.Logger import logger


class TestArticle:
    def test_create_table(self):
        ormutils.create_table(Article)

    def test_article(self):
        article = Article.create(
            website="test",
            kind="test",
            publish_date="09 02 2022",
            body="<br>adadwa<br><p></p>", title="hello",
            url="https://www.baidu.com",
            author=None,
            keyword=None,
            attachment="https://www.baidu.com"
        )
        article.save()
        logger.info(article.body)

        logger.info(article.ch_text)
