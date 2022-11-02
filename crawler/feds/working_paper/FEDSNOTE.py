from crawler.base_runner import BaseRunner
import datetime
from bs4 import BeautifulSoup
from common.Logger import *
from model.article import Article
import re
from common.timetransformer import TimeTransformer
from utils.ormutils import create_table


class FEDSNOTESWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(FEDSNOTESWorkingPaperRunner, self).__init__(
            website="FEDSNOTES",
            kind="working_paper",
            home_url="https://www.federalreserve.gov/econres/notes/feds-notes/default.htm"
        )

    def get_page_num(self):
        """
        FEDS按照年份分，最早的是2013
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        new_year = datetime.datetime.now().year
        old_year = 2013
        return new_year - old_year + 1

    def get_one_list(self, year):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对IFDP网站
        :param year: 导航页的年份
        :return: 所有Page页面的url
        """

        # pagenums = self.get_page_num()

        logger.info(f"reading urls of {year} now,totally {2013}~{datetime.datetime.now().year} in all.")

        guide_url = f"https://www.federalreserve.gov/econres/notes/feds-notes/{year}-index.htm"

        response = self.session.get(guide_url)
        headers = {'Connection': 'close'}
        response.headers = headers
        html = BeautifulSoup(response.content, "html.parser")

        # 查找htm数据的网址
        htm_urls = html.select("div[id=article] div div h5 a")

        pagenums = self.get_page_num()
        urls = []

        # 构建指向page的网址
        pre = 'https://www.federalreserve.gov'
        for html_label in htm_urls:
            href = html_label.get('href')
            if href[:4] == "http":
                urls.append(href)
            else:
                urls.append(pre + href)
        logger.info(f"get urls from {guide_url} successfully, get {len(urls)} urls in all.")
        return urls

    def parse_page(self, url):
        """
        提取文章信息,feds网站2013~2016年和2017~现在的page html不一样，只能写成两种抽取方法
        :param article_url: 文章的网址
        :return:提取的信息
        """

        def parse_page_style1(url):
            """
            提取文章信息,feds网站2013~2016的page html不一样，只能写成两种抽取方法
            :param article_url: 文章的网址
            :return:提取的信息
            """
            # 建立查询
            response = self.session.get(url)
            response.encoding = 'utf-8'
            headers = {'Connection': 'close'}
            response.headers = headers
            data = BeautifulSoup(response.content, "html.parser")

            # 拿到正文html源码
            html_data_part = data.select("div[id=main]")

            # 寻找body
            if len(html_data_part) == 0:
                return None
            else:
                body = html_data_part[0]
                paras = body.find_all("p", recursive=False)
                body = "<div>" + "\n".join(list(map(str, paras))) + "</div>"

            # 拿到url
            art_url = url

            # 作者
            authors_html = data.select("div[id=layout] div[id=main]")[0]
            org_lst = authors_html.text.strip().split("\n")
            lst = []
            for x in org_lst:
                if x != '' and x != "\r":
                    lst.append(x.strip())
            logger.info(lst)

            # 拿到标题
            title = lst[1]

            authors = lst[2]

            # 日期
            publish_date = lst[0]
            try:
                publish_date = TimeTransformer.strtimeformat(publish_date, "%B %d, %Y")
            except:
                publish_date = None

            # 拿到keywords,该网站并没有
            keywords = None

            # 附件,没有对应的pdf
            attachment_url = None
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

        def parse_page_style2(url):
            """
            提取文章信息,feds网站和2017~现在的page html不一样，只能写成两种抽取方法
            :param url: 文章的网址
            :return:提取的信息
            """
            # 建立查询
            response = self.session.get(url)
            response.encoding = 'utf-8'
            headers = {'Connection': 'close'}
            response.headers = headers
            data = BeautifulSoup(response.content, "html.parser")
            # 拿到标题
            title = data.find("meta", property="og:title")
            if title is not None:
                title = title.get("content").strip()
            # 拿到正文html源码
            html_data_part = data.select("div[class=row] div[class='col-xs-12 col-md-8 col-sm-12']")
            html_data_p = html_data_part[0].select("p")

            # 寻找body

            body = html_data_part[0]
            # 有文章没有Summary，直接空着了
            if len(body.text) < 20:
                body = None
            else:
                tag_lst = body.find_all(recursive=False)[3:]
                body = []
                for tag in tag_lst:
                    # 丢弃div块
                    if not "div" in tag.name:
                        body.append(str(tag))

                body = "<div>" + "\n".join(body) + "</div>"

            # 拿到url
            art_url = url

            # 作者
            authors = html_data_p[1].text.strip()

            # 日期的class标签都是pub-desc hide
            publish_date = html_data_p[0].text.strip()
            publish_date = TimeTransformer.strtimeformat(publish_date, "%B %d, %Y")

            # 拿到keywords,该网站并没有
            keywords = None

            # 附件,没有对应的pdf
            attachment_url = None

            # 存储到结构体
            saved_data = Article(
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

        # pattern = r"\d{4}"
        # # 获取年份信息
        # year = int(re.findall(pattern, url)[0])

        to_save = parse_page_style1(url)
        if to_save is not None:
            return to_save
        else:
            to_save2 = parse_page_style2(url)
            if to_save2 is None:
                raise Exception
            return to_save2
