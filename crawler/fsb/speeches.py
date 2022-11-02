from bs4 import BeautifulSoup

from common.Logger import logger
from common.timetransformer import TimeTransformer
from crawler.base_runner import BaseRunner
from model.article import Article
from utils.ormutils import create_table


class FSBSpeechesRunner(BaseRunner):
    def __init__(self):
        super(FSBSpeechesRunner, self).__init__(
            website="FSB",
            kind="speech",
            home_url="https://www.fsb.org/press/speeches-and-statements/"
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

    def parse_page(self, url, after_date):
        """
        提取文章信息
        :param url: 文章的网址
        :return:提取的信息
        """
        # 建立查询
        response = self.session.get(url)
        response.encoding = 'utf-8'
        data = BeautifulSoup(response.content, "html.parser")

        # 数据库已经存在的文章
        urls_in_db = (Article
                      .select(Article.url)
                      .where((Article.website == self.website) & (Article.kind == self.kind))
                      .order_by(Article.publish_date.desc())
                      )
        urls_in_db = [x.url for x in urls_in_db]

        arts = data.select("div[class=media-body]")
        for art in arts:
            # 拿到标题
            title = art.find("a").text
            # 拿到时间
            publish_date = art.find("span", class_="media-date pull-right").text
            publish_date = TimeTransformer.strtimeformat(publish_date, "%d %B %Y")
            # 拿到正文html源码
            body = art.find("span", class_="media-excerpt")

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

            # 网址已经在数据库中
            if art_url in urls_in_db:
                logger.info("数据库已存在该文章，结束爬取")
                return

            if publish_date < after_date:
                logger.info(f"当前爬取的文章日期为{publish_date},早于限定日期{after_date},爬取结束")
                return

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
            saved_data.save()
            logger.info("get temp article information successfully")
            # logger.info(saved_data.display())

    def get_list(self, start_from=1, end_at=None):
        if end_at is None:
            end_at = self.get_page_num() + start_from
        res = []
        for i in range(start_from, end_at):
            res.extend(self.get_one_list(i))
        return res

    def run(self, after_date="2022-09-01", start_from=1, end_at=None):
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
            self.parse_page(url, after_date)
