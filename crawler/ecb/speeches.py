from crawler.base_runner import BaseRunner
import datetime
from bs4 import BeautifulSoup
from common.Logger import *
from model.article import Article
from common.timetransformer import TimeTransformer


class ECBSpeechesRunner(BaseRunner):
    def __init__(self):
        super(ECBSpeechesRunner, self).__init__(
            website="ECB",
            type="speech",
            home_url="https://www.ecb.europa.eu/press/key/speaker/pres/html/index.en.html"
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

        pubdata = data.find(class_="ecb-publicationDate")
        if len(pubdata) > 0:
            # 拿到时间
            pubdata = pubdata.text.split(",")
            publish_date = pubdata[-1].strip()

            publish_date = TimeTransformer.strtimeformat(publish_date, "%d %B %Y")
        else:
            pubdata = None

        # 拿到正文html源码
        body = data.select("main div[class=section]")
        if body is None:
            raise Exception("hmtl code lost")

        # 拿到url
        art_url = url

        # 拿到作者
        authors = ",".join(pubdata[:-1]).strip()

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
        saved_data = Article.create(
            website=self.website,
            type=self.type,
            publish_date=publish_date,
            body=body,
            title=title,
            url=art_url,
            author=authors,
            keyword=keywords,
            attachment=attachment_url
        )

        # logger.info(saved_data.display())
        logger.info("get temp article information successfully")
        return saved_data
