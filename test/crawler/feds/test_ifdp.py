from unittest import TestCase
from crawler.feds.working_paper.IFDP import IFDPWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = IFDPWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run(start_from=2022,end_at=2021)
        logger.info(res)
