from abc import abstractmethod
import requests

from common.Logger import logger



class BaseRunner:

    def __init__(self, name, home_url):
        self.name = name
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

    def get_list(self, start_from=1):
        total_page_num = self.get_page_num()
        res = []
        for i in range(start_from, total_page_num + 1):
            res.extend(self.get_one_list(i))
        return res

    def run(self):
        """
        把上面两个函数跑通
        :return:
        """
        logger.info("开始爬取 {}: {}", self.name, self.home_url)

        urls = self.get_list()
        logger.info("获取列表 {}", len(urls))

        articles = []
        n_articles = len(urls)
        f = open("output.txt", "a", encoding="utf-8")
        for i, url in enumerate(urls):
            logger.info("({}/{}) 爬取文章: {}", i + 1, n_articles, url)
            article = self.parse_page(url)
            articles.append(article)
            f.write("-" * 100)
            f.write("\n\n\n")
            f.write(article.__str__())
            f.write("\n\n\n")
            f.write("-" * 100)
        f.close()
        # TODO: save article

        return articles
