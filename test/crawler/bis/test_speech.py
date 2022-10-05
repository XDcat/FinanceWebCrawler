from unittest import TestCase
from crawler.bis.speeches import BISSpeechesRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = BISSpeechesRunner()

    def test_run(self):
        res = self.runner.run(end_at=2)
        logger.info(res)
