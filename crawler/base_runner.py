# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2022/9/21
__project__ = FinanceWebCrawler
Fix the Problem, Not the Blame.
'''
from abc import abstractmethod
from common.Logger import logger
import time
import requests

class BaseRunner:
    def __init__(self, name, home_url):
        self.name = name
        self.home_url = home_url
        self.session = requests.Session()

    @abstractmethod
    def get_page_num(self):
        pass

    @abstractmethod
    def get_one_list(self, page:int):
        pass

    def get_list(self, start_from=0):
        page_num = self.get_page_num()
        res = []
        for i in range(start_from, page_num + start_from):
            res.append(self.get_page_num(i))
        return res


    @abstractmethod
    def parse_page(self, url):
        pass

    def run(self, sleep=1):
        logger.info("开始爬取 {}: {}", self.name, self.home_url)

        urls = self.get_list()
        logger.info("获取列表 {}", len(urls))

        articles = []
        n_articles = len(urls)
        for i, url in enumerate(urls):
            logger.info("({}/{}) 爬取文章: {}", i + 1, n_articles, url)
            article = self.parse_page(url)
            articles.append(article)

            time.sleep(sleep)
            # TODO: save article

        return articles
