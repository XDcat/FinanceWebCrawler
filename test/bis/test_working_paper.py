from unittest import TestCase
from FinanceWebCrawler.crawler.bis.working_paper import BISWorkingPaperRunner
from FinanceWebCrawler.common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = BISWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run()
        logger.info(res)
