from unittest import TestCase

from common.Logger import logger
from crawler.fsb.speeches import FSBSpeechesRunner


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = FSBSpeechesRunner()

    def test_run(self):
        res = self.runner.run(start_from=1, end_at=3)
        logger.info(res)
