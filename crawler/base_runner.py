import time
from abc import abstractmethod
import requests

from common.Logger import logger
from model.article import Article
from utils.ormutils import create_table


class BaseRunner:

    def __init__(self, website, kind, home_url):
        self.website = website
        self.kind = kind
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

        # 如果是年份表示start_from
        if start_from > 1500:
            if end_at is None:
                end_at = start_from - self.get_page_num()

            res = []
            for year in range(start_from, end_at, -1):
                res.extend(self.get_one_list(year))
            return res

        else:
            if end_at is None:
                end_at = self.get_page_num() + start_from

            res = []
            for i in range(start_from, end_at):
                res.extend(self.get_one_list(i))
            return res

    def run(self, after_date="2022-09-01", start_from=1, end_at=None):
        """
        爬取文章导入数据库
        :param after_date: 文章的最早日期
        :param start_from: 开始爬取的页数
        :param end_at: 结束页数
        :return:
        """
        create_table(Article)
        logger.info("开始爬取 {}: {}", self.website + self.kind, self.home_url)

        # 如果start_From是年份
        urls = self.get_list(start_from=start_from, end_at=end_at)
        # 删除数据库已经有的url
        urls_in_db = (Article
                      .select(Article.url)
                      .where((Article.website == self.website) & (Article.kind == self.kind))
                      .order_by(Article.publish_date.desc())
                      )
        urls_in_db = [x.url for x in urls_in_db]
        index = 0
        for index in range(len(urls)):
            # 数据库中最新的文章url
            if urls[index] in urls_in_db:
                urls = urls[0:index]
                break

        if index == 0:
            logger.info("数据库文章已经最新，无需更新")
            return
        else:
            logger.info(f"新的文章有{len(urls)}篇")

        logger.info("获取列表 {}", len(urls))

        n_articles = len(urls)
        for i, url in enumerate(urls):
            logger.info("({}/{}) 爬取文章: {}", i + 1, n_articles, url)
            time.sleep(0.5)
            article = self.parse_page(url)
            # 文章晚于限定的日期，才保存
            if article.publish_date >= after_date:
                Article.save(article)
            else:
                logger.info(f"当前爬取的文章日期为{article.publish_date},早于限定日期{after_date},爬取结束")
                return
