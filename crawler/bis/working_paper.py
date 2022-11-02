import requests
from bs4 import BeautifulSoup
from crawler.base_runner import BaseRunner
from common.Logger import logger
from model.article import Article
from common.timetransformer import TimeTransformer


class BISWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(BISWorkingPaperRunner, self).__init__(
            website="BIS",
            kind="working_paper",
            home_url="https://www.bis.org/wpapers/index.htm?m=1026"
        )

    def get_page_num(self):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        # 建立查询
        response = self.session.get(self.home_url)
        response.encoding = 'utf-8'

        html = BeautifulSoup(response.content, "html.parser")
        # 查找htm数据的网址
        htm_url = html.find('div', class_="bisobj_document_list").get('data-document_list_url')
        htm_url = "https://www.bis.org" + htm_url

        # 获取导航页最多页数

        # 建立查询
        response1 = self.session.get(htm_url)
        response1.encoding = 'utf-8'
        # 查找页码
        first_page_html = BeautifulSoup(response1.content, "html.parser")
        div = first_page_html.find('div', class_='pageof')
        numstring = div.find("span").text
        lst = numstring.split(' ')
        logger.info("complete max pages num search,outcome is {}", int(lst[2]))
        return int(lst[2])

    def get_one_list(self, page_num):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """
        # 建立查询
        response = self.session.get(self.home_url)

        html = BeautifulSoup(response.content, "html.parser")
        # 查找htm数据的网址
        htm_url = html.find('div', class_="bisobj_document_list").get('data-document_list_url')
        htm_url = "https://www.bis.org" + htm_url

        pagenums = self.get_page_num()

        urls = []
        logger.info(f"reading page{page_num} now,totally {pagenums} in all.")

        response1 = self.session.get(htm_url, params={"page": page_num})
        response1.encoding = 'utf-8'
        article_list = BeautifulSoup(response1.content, "html.parser")
        article_url_list = article_list.find_all("div", class_='title')
        # 构建指向page的网址
        pre = 'https://www.bis.org'
        for html_label in article_url_list:
            href = html_label.find('a').get('href')
            urls.append(pre + href)
        logger.info(f"get urls successfully,url={self.home_url}, get {len(urls)} urls in all.")
        return urls

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
        # 拿到标题
        title = data.find("title").text
        # 拿到时间
        publish_date = data.find("div", class_="date").text
        publish_date = TimeTransformer.strtimeformat(publish_date, "%d %B %Y")

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
        saved_data = Article(
            website=self.website,
            kind=self.kind,
            publish_date=publish_date,
            body=body,
            title=title,
            url=url,
            author=authors,
            keyword=keywords,
            attachment=attachment_url
        )
        logger.info("get temp article information successfully")
        return saved_data
