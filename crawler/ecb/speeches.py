import time

from bs4 import BeautifulSoup

from common.Logger import *
from common.timetransformer import TimeTransformer
from crawler.base_runner import BaseRunner
from model.article import Article
from utils.ormutils import create_table


class ECBSpeechesRunner(BaseRunner):
    def __init__(self):
        super(ECBSpeechesRunner, self).__init__(
            website="ECB",
            kind="speech",
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
        if pubdata is not None:
            # 拿到时间
            pubdata = pubdata.text.split(",")
            publish_date = pubdata[-1].strip()
            # 拿到作者
            # authors = ",".join(pubdata[:-1]).strip()
            publish_date = TimeTransformer.strtimeformat(publish_date, "%d %B %Y")
        else:
            # 另一种格式的
            pubdata = data.find(class_="ecb-pressContentSubtitle")
            if pubdata is not None:
                pubdata = pubdata.text.split(",")
                publish_date = pubdata[-1].strip()
                try:
                    publish_date = TimeTransformer.strtimeformat(publish_date, "%d %B %Y")
                except ValueError as v:
                    publish_date = None
                # authors = pubdata[0].strip()
            else:
                publish_date = None
                # authors = None

        # 拿到作者
        author_html = data.select("h2")
        if len(author_html) > 0:
            author_string = author_html[0].text.strip().split(",")
            if len(author_string) > 0:
                authors = author_string[0].split("by")
                if len(authors) > 1:
                    authors = authors[1].strip()
                else:
                    authors = authors[0].strip()

        # 拿到正文html源码
        body = data.select("main div[class=section]")
        if len(body) > 0:
            body = body[0]
            body = "<div>" + "\n".join(list(map(str, body.find_all(recursive=False)))[2:]) + "</div>"
        else:
            body = None

        # 拿到url
        art_url = url

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

    def run(self, after_date="2022-09-01", start_from=1, end_at=None):
        """
        把上面两个函数跑通
        :return:
        """
        create_table(Article)
        logger.info("开始爬取 {}: {}", self.website + self.kind, self.home_url)

        urls = self.get_list(start_from=start_from, end_at=end_at)
        # 删除数据库已经有的url
        urls_in_db =(Article
                    .select(Article.url)
                    .where((Article.website ==self.website)&(Article.kind==self.kind))
                    .order_by(Article.publish_date.desc())
                    )
        urls_in_db =[x.url for x in urls_in_db]
        index=0
        for index in range(len(urls)):
            # 数据库中最新的文章url
            if urls[index] in urls_in_db:
                urls=urls[0:index]
                break

        if index==0:
            logger.info("数据库文章已经最新，无需更新")
            return
        else:
            logger.info(f"新的文章有{len(urls)}篇")


        logger.info("获取列表 {}", len(urls))

        n_articles = len(urls)
        for i, url in enumerate(urls):
            logger.info("({}/{}) 爬取文章: {}", i + 1, n_articles, url)
            time.sleep(1)
            article = self.parse_page(url)
            # 文章晚于限定的日期，才保存
            if article.publish_date>=after_date:
                Article.save(article)
            else:
                logger.info(f"当前爬取的文章日期为{article.publish_date},早于限定日期{after_date},爬取结束")
                break

