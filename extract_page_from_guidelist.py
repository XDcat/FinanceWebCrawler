from bs4 import BeautifulSoup

from connector import Connector
from common.Logger import logger


class DetectGuideList:

    @staticmethod
    def read_page_from_list(list_page_url, pagenums=5, use_date=False, from_date=None, till_date=None):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param list_page_url:导航页面的Url
        :param pagenums:浏览导航页的数目
        :param use_date:是否指定日期范围
        :param from_date:文章的最早发布日期，请按照"YYYY-MM-DD"的格式输入
        :param till_date:文章的最晚发布日期，请按照"YYYY-MM-DD"的格式输入
        :return: 所有Page页面的url
        """
        assert type(list_page_url) == str
        # 建立查询
        response = Connector.connectToUrl(list_page_url, encoding='utf-8', method="get")
        html = BeautifulSoup(response.content, "html.parser")
        # 查找htm数据的网址
        htm_url = html.find('div', class_="bisobj_document_list").get('data-document_list_url')
        htm_url = "https://www.bis.org" + htm_url
        # 时间选择模块
        if use_date is True:
            # 按照body结构体的参数格式传
            year_f, month_f, day_f = from_date.split('-')
            year_t, month_t, day_t = till_date.split('-')
            standard_from_time = day_f + '/' + month_f + '/' + year_f
            standard_till_time = day_t + '/' + month_t + '/' + year_t
            record = []
            for i in range(1, pagenums + 1):
                # 访问htm数据，这也是个html,采用post方法,将参数传给body
                response1 = Connector.connectToUrl(htm_url, params={"page": i, 'from': standard_from_time,
                                                                    'till': standard_till_time})
                article_list = BeautifulSoup(response1.content, "html.parser")
                article_url_list = article_list.find_all("div", class_='title')
                # 构建指向page的网址
                pre = 'https://www.bis.org'
                for html_label in article_url_list:
                    href = html_label.find('a').get('href')
                    record.append(pre + href)
            logger.info("readPagefromList success,url={},{} in all.", list_page_url, len(record))
            return record

        else:
            record = []
            for i in range(1, pagenums + 1):
                # 访问htm数据，这也是个html,采用post方法,将参数传给body
                response1 = Connector.connectToUrl(htm_url, params={"page": i})
                article_list = BeautifulSoup(response1.content, "html.parser")
                article_url_list = article_list.find_all("div", class_='title')
                pre = 'https://www.bis.org'
                for html_label in article_url_list:
                    href = html_label.find('a').get('href')
                    record.append(pre + href)
            logger.info("readPagefromList success,url={},{} in all.", list_page_url, len(record))
            return record
