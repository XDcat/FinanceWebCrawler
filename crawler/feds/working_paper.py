from crawler.base_runner import BaseRunner
import datetime
from bs4 import BeautifulSoup
from common.Logger import *
from model.article import Article


class FEDSWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(FEDSWorkingPaperRunner, self).__init__(
            "FEDS working papers",
            "https://www.federalreserve.gov/econres/feds/index.htm"
        )

    def get_page_num(self):
        """
        ecb按照年份分，最早的是1996
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        new_year = datetime.datetime.now().year
        old_year=1996
        return new_year-old_year+1

    def get_one_list(self, year):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对FEDE网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """

        # 访问htm数据，这也是个html,采用post方法,将参数传给body
        htm_url = f"https://www.federalreserve.gov/econres/feds/{year}.htm"
        # 嵌套拿取网址
        # pagenums = self.get_page_num()

        logger.info(f"reading urls of {year} now,totally {1996}~{datetime.datetime.now().year} in all.")

        guide_url=f"https://www.federalreserve.gov/econres/feds/{year}.htm"

        response = self.session.get(guide_url)

        html = BeautifulSoup(response.content, "html.parser")

        # 查找htm数据的网址
        htm_urls = html.select("div div h5 a")

        pagenums = self.get_page_num()
        urls=[]

        # 构建指向page的网址
        pre = 'https://www.federalreserve.gov'
        for html_label in htm_urls:
            href = html_label.get('href')
            urls.append(pre + href)
        logger.info(f"get urls from {guide_url} successfully, get {len(urls)-1} urls in all.")
        # 第一个是原网址
        return urls[1:]

    def parse_page(self, url):
        """
        提取文章信息
        :param article_url: 文章的网址
        :return:提取的信息
        """
        # 建立查询
        response = self.session.get(url)
        response.encoding = 'utf-8'
        data = BeautifulSoup(response.content, "html.parser")
        # 拿到标题
        title = data.find('div', id="page-title")
        if title is not None:
            title=title.text.strip()
        # 拿到正文html源码
        html_data_part = data.select("div[class=row] div[class='col-lg-8 col-md-8 col-sm-12 col-xs-12'] p")

        body=html_data_part[3]
        # 有文章没有Summary，直接空着了
        if len(body.text)<20:
            body=None


        # 拿到url
        art_url = url

        #作者
        authors=html_data_part[1].text.strip()

        # 日期的class标签都是pub-desc hide
        publish_date =html_data_part[0].text.strip()

        # 拿到keywords,该网站并没有
        keywords = None

        # 附件
        pre="https://www.federalreserve.gov"
        for i in range(3,len(html_data_part)):
            if html_data_part is not None:
                textt=html_data_part[i].text
                if "PDF" in textt:
                    attachment_url = html_data_part[i].find("a")

        if attachment_url:
            attachment_url=pre+attachment_url.get("href")

        # 存储到结构体
        saved_data = Article(publish_date, body, title, art_url, authors, keywords, attachment_url)
        logger.info(saved_data.display())
        # 中文文本
        # ch_text = saved_data.get_ch_text
        logger.info("get temp article information successfully")
        return saved_data

    def get_list(self, start_from=1996):
        total_page_num = self.get_page_num()
        res = []
        for i in range(start_from, start_from+total_page_num ):
            res.extend(self.get_one_list(i))
        return res
