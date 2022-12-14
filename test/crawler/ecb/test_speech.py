from unittest import TestCase
from crawler.ecb.speeches import ECBSpeechesRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = ECBSpeechesRunner()

    def test_run(self):
        res = self.runner.run()
        logger.info(res)
