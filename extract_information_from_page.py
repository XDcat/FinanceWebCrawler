from bs4 import BeautifulSoup

from connector import Connector
from model.article import Article
from common.Logger import logger


class ExtractInfFromPage:

    @staticmethod
    def extract_message_from_article(article_url):
        """ 提取文章信息
        :param article_url: 文章的网址
        :return:提取的信息
        """
        response = Connector.connectToUrl(article_url)
        data = BeautifulSoup(response.content, "html.parser")
        # 拿到标题
        title = data.find("title")
        # 拿到时间
        publish_date = data.find("div", class_="date")
        # 拿到正文html源码
        body = data.find("div", id="cmsContent")
        # 拿到url
        art_url = data.find("meta", property="og:url").get("content")
        # 拿到作者
        author_list = data.find_all('div', class_="authorname")
        authors = ", ".join([author_div.text for author_div in author_list])
        # 拿到keywords
        keywords = data.find("meta", attrs={"name": "keywords"}).get("content")
        # 拿到附件
        attachment_url = data.find("a", class_="pdftitle_link").get("href")
        # 合并
        attachment_url = "https://www.bis.org" + attachment_url
        # 存储到结构体
        saved_data = Article(publish_date, body, title, art_url, authors, keywords, attachment_url)
        logger.info("read and write article information successfully")

        return saved_data
