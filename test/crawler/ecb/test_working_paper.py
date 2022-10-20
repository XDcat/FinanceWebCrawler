from unittest import TestCase
from crawler.ecb.working_paper import ECBWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = ECBWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run(start_from=2022,end_at=2021)
        logger.info(res)

    def test_parse(self):
        url="https://www.ecb.europa.eu/pub/research/working-papers/html/papers-2022.include.en.html"
        self.runner.parse_page(url)