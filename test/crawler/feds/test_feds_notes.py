from unittest import TestCase
from crawler.feds.working_paper.FEDSNOTE import FEDSNOTESWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = FEDSNOTESWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run()
        logger.info(res)
