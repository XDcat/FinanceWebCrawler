from abc import abstractmethod
import requests

from common.Logger import logger
from model.article import Article
from utils.ormutils import create_table


class BaseRunner:

    def __init__(self, website, type, home_url):
        self.website = website
        self.type = type
        self.home_url = home_url
        self.session = requests.Session()

    @abstractmethod
    def parse_page(self, url):
        """
        获取articlepage的详细数据
        :param url:
        :return:
        """

    @abstractmethod
    def get_page_num(self):
        """
        获取页面最大页数
        :return: 页数
        """
        pass

    @abstractmethod
    def get_one_list(self, pagenum: int):
        """
        获取某一页的urls
        :param pagenum: 页码
        :return: urls
        """
        pass

    def get_list(self, start_from=1, end_at=None):
        if end_at is None:
            end_at = self.get_page_num() + start_from

        res = []
        for i in range(start_from, end_at):
            res.extend(self.get_one_list(i))
        return res

    def run(self, start_from=1, end_at=None):
        """
        把上面两个函数跑通
        :return:
        """
        create_table(Article)
        logger.info("开始爬取 {}: {}", self.website + self.type, self.home_url)

        urls = self.get_list(start_from=start_from, end_at=end_at)
        logger.info("获取列表 {}", len(urls))

        n_articles = len(urls)
        for i, url in enumerate(urls):
            logger.info("({}/{}) 爬取文章: {}", i + 1, n_articles, url)
            article = self.parse_page(url)
            Article.save(article)
