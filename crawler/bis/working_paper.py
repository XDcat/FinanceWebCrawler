# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2022/9/21
__project__ = FinanceWebCrawler
Fix the Problem, Not the Blame.
'''
import requests
from bs4 import BeautifulSoup

from connector import Connector
from crawler.base_runner import BaseRunner
from common.Logger import logger
from model.article import Article


class BISWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(BISWorkingPaperRunner, self).__init__(
            "BIS working paper",
            "https://www.bis.org/wpapers/index.htm?m=1026"
        )
    def get_page_num(self):
        """
        获取导航页最多页数
        :param url: 导航页网址
        :return:
        """
        # 建立查询
        session = requests.session()
        response1 = session.get(self.home_url)
        response1.encoding = 'utf-8'
        # 查找页码
        first_page_html = BeautifulSoup(response1.content, "html.parser")
        div = first_page_html.find('div', class_='pageof')
        numstring = div.find("span").text
        lst = numstring.split(' ')
        logger.info("complete max pages num search,outcome is {}", int(lst[2]))
        return int(lst[2])

    def get_one_list(self, page):
        # TODO: 获取单页的 url list
        # page: 页码
        pass


    def parse_page(self, url):
        """
        提取文章信息
        :param article_url: 文章的网址
        :return:提取的信息
        """
        # 建立查询
        session = requests.session()
        response = session.get(url)
        response.encoding = 'utf-8'
        data = BeautifulSoup(response.content, "html.parser")
        # 拿到标题
        title = data.find("title")
        # 拿到时间
        publish_date = data.find("div", class_="date")

        # 拿到正文html源码
        body = data.find("div", id="cmsContent")
        if body is None:
            raise Exception("hmtl code lost")

        # 拿到url
        art_url = data.find("meta", property="og:url")
        if art_url is not None:
            art_url = art_url.get("content")

        # 拿到作者
        author_list = data.find_all('div', class_="authorname")
        if author_list is not None:
            authors = ", ".join([author_div.text for author_div in author_list])
        else:
            authors = None

        # 拿到keywords
        keywords = data.find("meta", attrs={"name": "keywords"})
        if keywords is not None:
            keywords = keywords.get("content")

        # 拿到附件
        attachment_url = data.find("a", class_="pdftitle_link")
        if attachment_url is not None:
            attachment_url = attachment_url.get("href")

        # 合并
        attachment_url = "https://www.bis.org" + attachment_url
        # 存储到结构体
        saved_data = Article(publish_date, body, title, art_url, authors, keywords, attachment_url)
        # 中文文本
        # ch_text = saved_data.get_ch_text
        logger.info("get temp article information successfully")
        return saved_data
