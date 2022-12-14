from crawler.base_runner import BaseRunner
import datetime
from bs4 import BeautifulSoup
from common.Logger import *
from model.article import Article
from common.timetransformer import TimeTransformer
from utils.ormutils import create_table


class FEDSWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(FEDSWorkingPaperRunner, self).__init__(
            website="FEDS",
            kind="working_paper",
            home_url="https://www.federalreserve.gov/econres/feds/index.htm"
        )

    def get_page_num(self):
        """
        feds按照年份分，最早的是1996
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        new_year = datetime.datetime.now().year
        old_year = 1996
        return new_year - old_year + 1

    def get_one_list(self, year):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对FEDE网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """

        # 访问htm数据，这也是个html,采用post方法,将参数传给body
        # 嵌套拿取网址
        # pagenums = self.get_page_num()

        logger.info(f"reading urls of {year} now,totally {1996}~{datetime.datetime.now().year} in all.")

        guide_url = f"https://www.federalreserve.gov/econres/feds/{year}.htm"

        response = self.session.get(guide_url)

        html = BeautifulSoup(response.content, "html.parser")

        # 查找htm数据的网址
        htm_urls = html.select("div div h5 a")

        pagenums = self.get_page_num()
        urls = []

        # 构建指向page的网址
        pre = 'https://www.federalreserve.gov'
        for html_label in htm_urls:
            href = html_label.get('href')
            urls.append(pre + href)
        logger.info(f"get urls from {guide_url} successfully, get {len(urls) - 1} urls in all.")
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
        title = data.select("title")
        if len(title) > 0:
            title = title[0].text.strip()
        else:
            title = None
        # 拿到正文html源码
        html_data_part = data.select("div[class=row] div[class='col-lg-8 col-md-8 col-sm-12 col-xs-12'] p")

        body = data.select("div[class=row] div[class='col-lg-8 col-md-8 col-sm-12 col-xs-12']")[0]
        # 有文章没有Summary，直接空着了
        if len(body.text) < 40:
            body = None
        else:
            tag_lst = body.find_all(recursive=False)[4:]
            body = []
            special_word=("pdf","abstract","doi","related materials","keywords")
            for tag in tag_lst:
                # 丢弃div块
                if not "div" in tag.name:
                    if tag.strong is not None:
                        # strong标签内的标题转换为小写
                        temp=tag.strong.text.lower()
                        flag=0
                        for word in special_word:
                            if word in temp:
                                flag=1
                                break
                        if flag==0:
                            body.append(str(tag))
                    else:
                        body.append(str(tag))

                # 判断p标签内的strong标签内容，是否为pdf,abstract,doi,Related Materials,keywords

            body = "<div>" + "\n".join(body) + "</div>"

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

        # 附件
        pre = "https://www.federalreserve.gov"
        attachment_url = None
        for i in range(3, len(html_data_part)):
            if html_data_part is not None:
                textt = html_data_part[i].text
                if "PDF" in textt:
                    attachment_url = html_data_part[i].find("a")

        if attachment_url:
            attachment_url = pre + attachment_url.get("href")

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
