import requests
from bs4 import BeautifulSoup
from crawler.base_runner import BaseRunner
from common.Logger import logger
from model.article import Article
import time
from common.timetransformer import TimeTransformer
from utils.ormutils import create_table


class IMFWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(IMFWorkingPaperRunner, self).__init__(
            website="IMF",
            type="working_paper",
            home_url="https://www.imf.org/en/publications/search?when=After&series=IMF%20Working%20Papers"
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
        page_html = html.find("p", class_="pages")
        # 字符串拆分
        info_list = page_html.text.split()
        # 最大page就在页面上，html结构比较混乱
        pagenums = 0
        for i in range(len(info_list)):
            if info_list[i] == "of":
                pagenums = int(info_list[i + 1])
                break
        else:
            raise Exception("pagenums not found")
        return pagenums

    def get_one_list(self, page_num):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """
        # 建立查询
        response = self.session.get(self.home_url)
        response.encoding = 'utf-8'
        pagenums=self.get_page_num()
        logger.info(f"reading page{page_num} now,totally {pagenums} in all.")
        # 访问htm数据，这也是个html,采用post方法,将参数传给body
        htm_url = f"https://www.imf.org/en/publications/search?when=After&series=IMF%20Working%20Papers&page={page_num}"
        response1 = self.session.get(htm_url)
        response1.encoding = 'utf-8'
        # 嵌套拿取网址
        article_list = BeautifulSoup(response1.content, "html.parser")
        article_url_list = article_list.find_all("div", class_='result-row pub-row')
        urls = []
        pre = "https://www.imf.org/"
        # 构建指向page的网址
        for html_label in article_url_list:
            href = html_label.find('a').get('href')
            urls.append(pre + href)
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
        title = data.find('meta', property="og:title").get("content")
        # 拿到正文html源码,这个网站的html重复较多。只能按照文本长度筛一下了
        html_list = data.select("div[class=content] div[class=column-padding] section p[class=pub-desc]")
        index = -1
        max_len = 0
        for i in range(len(html_list)):
            if len(html_list[i].text) > max_len:
                max_len = len(html_list[i].text)
                index = i
        body = html_list[index]

        # 拿到url
        art_url = data.find("meta", property="og:url")
        if art_url is None:
            raise Exception("art_url is None")
        else:
            art_url = art_url.get("content")

        # 这个网站作者和日期的class标签都是pub-desc hide
        author_list, publish_date = data.find_all('p', class_="pub-desc hide")
        authors = "".join([author_div.text.strip() for author_div in author_list])

        publish_date = publish_date.text.strip()
        publish_date = TimeTransformer.strtimeformat(publish_date, "%B %d, %Y")

        # 拿到keywords
        keywords = data.find("meta", attrs={"name": "Keywords"})
        if keywords is not None:
            keywords = keywords.get("content")

        # 拿到附件
        attachment_url1 = data.select("section p[class=pub-desc] a")[0]
        if attachment_url1 is None:
            attachment_url2 = data.find("a", class_="piwik_download")
            if attachment_url2 is None:
                raise Exception("url not found")
            else:
                attachment_url = attachment_url2.get("href")
        else:
            attachment_url = attachment_url1.get("href")
        # 合并
        attachment_url = "https://www.imf.org" + attachment_url
        # 存储到结构体
        saved_data = Article.create(
            website=self.website,
            type=self.type,
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


    def run(self, start_from=1, end_at=None):
        """
        把上面两个函数跑通
        :return:
        """
        create_table(Article)
        logger.info("开始爬取 {}: {}", self.website + self.type, self.home_url)

        urls = self.get_list(start_from=start_from, end_at=end_at)
        logger.info("获取列表 {}", len(urls))

        n_articles = len(urls)
        for i, url in enumerate(urls):
            logger.info("({}/{}) 爬取文章: {}", i + 1, n_articles, url)
            time.sleep(1)
            article = self.parse_page(url)
            Article.save(article)