import requests
from bs4 import BeautifulSoup
from crawler.base_runner import BaseRunner
from common.Logger import logger
from model.article import Article


class FSBSpeechesRunner(BaseRunner):
    def __init__(self):
        super(FSBSpeechesRunner, self).__init__(
            "FSB speeches",
            "https://www.fsb.org/press/speeches-and-statements/"
        )

    def get_page_num(self):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对fsb网站
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        # 建立查询
        response = self.session.get(self.home_url)
        response.encoding = 'utf-8'

        html = BeautifulSoup(response.content, "html.parser")

        time = html.findAll("a", class_="page-numbers")
        return int(time[2].text)

    def get_one_list(self, page_num):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """
        guide_url = f"https://www.fsb.org/press/speeches-and-statements/?mt_page={page_num}"
        # 建立查询
        # response = self.session.get(guide_url,params={"page":page_num})
        #
        # html = BeautifulSoup(response.content, "html.parser")
        #
        # pagenums = self.get_page_num()
        #
        # urls = []
        # logger.info(f"reading page{page_num} now,totally {pagenums} in all.")
        #
        # article_url_list = html.select("h3[class=media-heading] a")
        # # 构建指向page的网址
        # for html_label in article_url_list:
        #     href = html_label.get('href')
        #     urls.append(href)
        # logger.info(f"get urls successfully,url={self.home_url}, get {len(urls)} urls in all.")
        return [guide_url]

    def parse_page(self, url):
        """
        提取文章信息
        :param url: 文章的网址
        :return:提取的信息
        """
        # 建立查询
        response = self.session.get(url)
        response.encoding = 'utf-8'
        data = BeautifulSoup(response.content, "html.parser")

        arts = data.select("div[class=media-body]")
        for art in arts:
            # 拿到标题
            title = art.find("a").text
            # 拿到时间
            publish_date = art.find("span", class_="media-date pull-right").text
            # 拿到正文html源码
            body = art.find("span", class_="media-excerpt").text.strip()

            # 拿到url
            art_url = art.find("a").get("href")

            # 拿到作者
            authors = None

            # 拿到keywords
            keywords = None

            # 拿到附件
            if "pdf" in art_url:
                attachment_url = art_url
            else:
                # 去网页找pdf是否存在
                response1 = self.session.get(art_url)
                response1.encoding = 'utf-8'
                information = BeautifulSoup(response1.content, "html.parser")
                attachment_url = information.select("div[class='post-formats lead']>a")
                if len(attachment_url) > 0:
                    attachment_url = attachment_url[0].get("href")
                else:
                    attachment_url = None

            # 存储到结构体
            saved_data = Article(publish_date, body, title, art_url, authors, keywords, attachment_url)
            logger.info("get temp article information successfully")
            # 中文文本
            # ch_text = saved_data.get_ch_text
            logger.info(saved_data.display())
