from unittest import TestCase
from crawler.feds.speeches import FEDSpeechesRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = FEDSpeechesRunner()

    def test_run(self):
        res = self.runner.run()
        logger.info(res)

    def test_parse(self):
        url = "https://www.federalreserve.gov/newsevents/speech/barr20220907a.htm"
        self.runner.parse_page(url)
