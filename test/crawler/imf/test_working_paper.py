from unittest import TestCase
from crawler.imf.working_paper import IMFWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = IMFWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run(end_at=3)
        logger.info(res)
