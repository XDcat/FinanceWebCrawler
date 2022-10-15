from crawler.base_runner import BaseRunner
import datetime
from bs4 import BeautifulSoup
from common.Logger import *
from model.article import Article
from common.timetransformer import TimeTransformer
from utils.ormutils import create_table


class IFDPWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(IFDPWorkingPaperRunner, self).__init__(
            website="IFDP",
            kind="working_paper",
            home_url="https://www.federalreserve.gov/econres/ifdp/index.htm"
        )

    def get_page_num(self):
        """
        ifdp按照年份分，最早的是1971
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        new_year = datetime.datetime.now().year
        old_year = 1971
        return new_year - old_year + 1

    def get_one_list(self, year):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对IFDP网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """

        # pagenums = self.get_page_num()

        logger.info(f"reading urls of {year} now,totally {1971}~{datetime.datetime.now().year} in all.")

        guide_url = f"https://www.federalreserve.gov/econres/ifdp/{year}.htm"

        response = self.session.get(guide_url)

        html = BeautifulSoup(response.content, "html.parser")

        # 查找htm数据的网址
        htm_urls = html.select("div[id=article] div div h5 a")

        pagenums = self.get_page_num()
        urls = []

        # 构建指向page的网址
        pre = 'https://www.federalreserve.gov'
        for html_label in htm_urls:
            href = html_label.get('href')
            urls.append(pre + href)
        logger.info(f"get urls from {guide_url} successfully, get {len(urls)} urls in all.")

        return urls

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
        title = data.find("title")
        if title is not None:
            title = title.text.strip()
        # 拿到正文html源码
        html_data_part = data.select("div[class=row] div[class='col-lg-8 col-md-8 col-sm-12 col-xs-12'] p")

        body = data.select("div[class=row] div[class='col-lg-8 col-md-8 col-sm-12 col-xs-12']")[0]
        # 有文章没有Summary，直接空着了
        if len(body.text) < 20:
            body = None

        # 拿到url
        art_url = url

        # 作者
        authors = html_data_part[1].text.strip()

        # 日期的class标签都是pub-desc hide
        publish_date_list = html_data_part[0].text.strip().split("\n")
        publish_date = publish_date_list[0].strip()
        publish_date = TimeTransformer.strtimeformat(publish_date, "%B %Y")

        # 拿到keywords,该网站并没有
        keywords = None

        attachment_url = None
        # 附件
        pre = "https://www.federalreserve.gov"
        for i in range(3, len(html_data_part)):
            if html_data_part is not None:
                textt = html_data_part[i].text
                if "PDF" in textt:
                    attachment_url = html_data_part[i].find("a")

        if attachment_url:
            attachment_url = pre + attachment_url.get("href")

        # 存储到结构体
        saved_data = Article.create(
            website=self.website,
            kind=self.kind,
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

    def get_list(self, start_from=2000, end_at=None):
        if end_at is None:
            end_at = self.get_page_num() + start_from
        res = []
        for i in range(start_from, end_at):
            res.extend(self.get_one_list(i))
        return res

    def run(self, start_from=2000, end_at=None):
        """
        把上面两个函数跑通
        :return:
        """
        create_table(Article)
        logger.info("开始爬取 {}: {}", self.website + self.kind, self.home_url)

        urls = self.get_list(start_from=start_from, end_at=end_at)
        logger.info("获取列表 {}", len(urls))

        n_articles = len(urls)
        for i, url in enumerate(urls):
            logger.info("({}/{}) 爬取文章: {}", i + 1, n_articles, url)
            article = self.parse_page(url)
            Article.save(article)


