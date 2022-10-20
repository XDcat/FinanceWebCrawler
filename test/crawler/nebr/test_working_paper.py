from unittest import TestCase
from crawler.nebr.working_paper import NEBRWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = NEBRWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run(start_from=1,end_at=5)
        logger.info(res)
