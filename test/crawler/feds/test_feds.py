from unittest import TestCase
from crawler.feds.working_paper.FEDS import FEDSWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = FEDSWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run()
        logger.info(res)
