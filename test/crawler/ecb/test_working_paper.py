from unittest import TestCase
from crawler.ecb.working_paper import ECBWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = ECBWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run()
        logger.info(res)
