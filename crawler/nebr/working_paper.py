from bs4 import BeautifulSoup
from crawler.base_runner import BaseRunner
from common.Logger import logger
from model.article import Article
from common.timetransformer import TimeTransformer


class NEBRWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(NEBRWorkingPaperRunner, self).__init__(
            website="NEBR",
            kind="working_paper",
            home_url="https://www.nber.org/papers?page=1&perPage=50&sortBy=public_date"
        )

        self.pagenums = self.get_page_num()

    def get_page_num(self):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        # 建立查询
        guide_url = "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=50&sortBy=public_date"
        response = self.session.get(guide_url)
        response.encoding = 'utf-8'

        dic = response.json()
        total_urls = dic.get("totalResults")
        if total_urls % 50 == 0:
            return total_urls // 50
        else:
            return total_urls // 50 + 1

    def get_one_list(self, page_num):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对NEBR网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """
        # 建立查询
        target_url = f"https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page={page_num}&perPage=50&sortBy=public_date"

        # 查找htm数据的网址

        pagenums = self.pagenums

        urls = []
        logger.info(f"reading page{page_num} now,totally {pagenums} in all.")

        response1 = self.session.get(target_url)
        response1.encoding = 'utf-8'
        headers = {'Connection': 'close'}
        response1.headers = headers
        data = response1.json().get("results")

        # 构建指向page的网址
        pre = 'https://www.nber.org'
        for art in data:
            url = art.get('url')
            urls.append(pre + url)
        logger.info(f"get urls successfully,url={target_url}, get {len(urls)} urls in all.")
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
        headers = {'Connection': 'close'}
        response.headers = headers
        data = BeautifulSoup(response.content, "html.parser")
        # 拿到标题
        title = data.find("meta", property="og:title").get("content")
        # 拿到时间
        publish_date = \
        data.select("div[class='page-header__citation-info'] div[class='page-header__citation-item'] time")[0].text
        publish_date = TimeTransformer.strtimeformat(publish_date, "%B %Y")

        # 拿到正文html源码
        body = data.find("div", class_="page-header__intro-inner")
        if body is None:
            raise Exception("hmtl code lost")

        # 拿到url
        art_url = url

        # 拿到作者
        authors = data.select("meta[name=keywords]")[0].get("content")

        # 拿到keywords
        keywords = None

        # 拿到附件
        attachment_url = data.select("meta[name='citation_pdf_url']")
        if len(attachment_url) > 0:
            attachment_url = attachment_url[0].get("content")

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
        logger.info("get temp article information successfully")
        return saved_data
