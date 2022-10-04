from unittest import TestCase
from crawler.fsb.speeches import FSBSpeechesRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = FSBSpeechesRunner()

    def test_run(self):
        res = self.runner.run(file_name="output_speech.txt")
        logger.info(res)
