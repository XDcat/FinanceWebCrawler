from unittest import TestCase
from crawler.feds.speeches import FEDSpeechesRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = FEDSpeechesRunner()

    def test_run(self):
        res = self.runner.run()
        logger.info(res)
