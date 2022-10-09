from unittest import TestCase
from controller.article_controller import ArticleController
from common.Logger import logger


class TestWorkingPaper(TestCase):

    def test_selector(self):
        selector = ArticleController()
        arts = selector.select_arts_from_db("2022-01-01", "2022-09-30", website="BIS", kind="speech")
        for ar in arts:
            print(ar.publish_date, ar.website, ar.kind)
        # logger.info(arts)
