from crawler.base_runner import BaseRunner
import datetime
from bs4 import BeautifulSoup
from common.Logger import *
from model.article import Article


class ECBSpeechesRunner(BaseRunner):
    def __init__(self):
        super(ECBSpeechesRunner, self).__init__(
            "ECB speeches",
            "https://www.ecb.europa.eu/press/key/speaker/pres/html/index.en.html"
        )

    def get_page_num(self):
        """
        ecb speeches只有一页
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        return 1

    def get_one_list(self, page_num):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """

        # 访问htm数据，这也是个html,采用post方法,将参数传给body
        htm_url = self.home_url
        response = self.session.get(htm_url)
        response.encoding = 'utf-8'
        data = BeautifulSoup(response.content, "html.parser")

        urls = []
        urls_html = data.select("main>div[class='definition-list -filter']>dl>dd>div[class=title] a")
        pre = "https://www.ecb.europa.eu"
        for url in urls_html:
            suffix = url.get("href")
            if "pdf" not in suffix:
                urls.append(pre + suffix)
        # 嵌套拿取网址
        # pagenums = self.get_page_num()

        logger.info(f"reading articles of page{page_num}  now,totally {self.get_page_num()} in all.")

        # 构建指向page的网址
        return urls

    def parse_page(self, url):
        """
        提取文章信息
        :param url: 文章的网址
        :return:提取的信息
        """
        """
        提取文章信息
        :param article_url: 文章的网址
        :return:提取的信息
        """
        # 建立查询
        response = self.session.get(url)
        response.encoding = 'utf-8'
        data = BeautifulSoup(response.content, "html.parser")
        headers = {'Connection': 'close'}
        response.headers = headers

        # 拿到标题
        title = data.find("title").text
        # 拿到时间
        publish_date = data.select("meta[name='citation_online_date']")
        if len(publish_date) > 0:
            publish_date = publish_date[0].get("content")
        else:
            publish_date = None

        # 拿到正文html源码
        body = data.select("main div[class=section]")
        if body is None:
            raise Exception("hmtl code lost")

        # 拿到url
        art_url = url

        # 拿到作者
        authors = data.select("meta[name=author]")[0].get("content")

        # 拿到keywords
        keywords = None

        # 拿到附件
        attachment_url = data.select("div[class=title] a")
        if len(attachment_url) > 0:
            attachment_url = attachment_url[0].get("href")
            pre = "https://www.ecb.europa.eu"
            attachment_url = pre + attachment_url
        else:
            attachment_url = None

        # 存储到结构体
        saved_data = Article(publish_date, body, title, art_url, authors, keywords, attachment_url)
        # 中文文本
        # ch_text = saved_data.get_ch_text
        logger.info(saved_data.display())
        logger.info("get temp article information successfully")
        return saved_data
