# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2022/9/21
__project__ = FinanceWebCrawler
Fix the Problem, Not the Blame.
'''

from unittest import TestCase
from crawler.bis.working_paper import BISWorkingPaperRunner
from common.Logger import logger


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = BISWorkingPaperRunner()

    def test_run(self):
        res = self.runner.run()
        logger.info(res)
