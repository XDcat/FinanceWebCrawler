from unittest import TestCase
from crawler.feds.working_paper.FEDS import FEDSWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = FEDSWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run(start_from=2022,end_at=2021)
        logger.info(res)

    def test_parse(self):
        self.runner.parse_page("https://www.federalreserve.gov/econres/feds/bank-deposit-flows-to-money-market-funds-and-on-rrp-usage-during-monetary-policy-tightening.htm")
