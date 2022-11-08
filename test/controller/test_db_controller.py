from unittest import TestCase
from controller.article_controller import ArticleController
from common.Logger import logger
from controller.db_controller import DbController


class TestWorkingPaper(TestCase):


    def test_translate_db(self):
        DbController.translate_db(overide=True)

    def test_generate_last_month_articles(self):
        ArticleController.generate_last_month_articles()
