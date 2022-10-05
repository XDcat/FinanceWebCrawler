from model.article import Article
from utils import ormutils

from common.Logger import logger


class TestArticle:
    def test_article(self):
        ormutils.create_table(Article)
        article = Article.create(
            website="BIS",
            type="working_paper",
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

    def test_instance(self):
        article = Article(
            publish_date="09 01 2022",
            body="<br>adadwa<br><p></p>", title="hello",
            url="https://www.baidu.com",
            author="me",
            keyword="yae",
            attachment="https://www.baidu.com"
        )
        article.save()
        logger.info(article.body)
        logger.info(article.ch_text)
