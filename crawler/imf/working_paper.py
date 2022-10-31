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
            kind="working_paper",
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
        pagenums = self.get_page_num()
        logger.info(f"reading page{page_num} now,totally {pagenums} in all.")
        # 访问htm数据，这也是个html,采用post方法,将参数传给body
        htm_url = f"https://www.imf.org/en/publications/search?when=After&series=IMF%20Working%20Papers&page={page_num}"
        response1 = self.session.get(htm_url)
        response1.encoding = 'utf-8'
        # 嵌套拿取网址
        article_list = BeautifulSoup(response1.content, "html.parser")
        article_url_list = article_list.find_all("div", class_='result-row pub-row')
        urls = []
        pre = "https://www.imf.org"
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
        body = "<div>" + str(html_list[index]) + "</div>"

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
        attachment_url1 = data.select("section p[class=pub-desc] a")
        if len(attachment_url1) == 0:
            attachment_url = None
        else:
            attachment_url1 = attachment_url1[0]
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

    def run(self, after_date="2022-09-01", start_from=1, end_at=None):
        """
        爬取文章导入数据库
        :param after_date: 文章的最早日期
        :param start_from: 开始爬取的页数
        :param end_at: 结束页数
        :return:
        """
        create_table(Article)
        logger.info("开始爬取 {}: {}", self.website + self.kind, self.home_url)

        # 如果start_From是年份
        urls = self.get_list(start_from=start_from, end_at=end_at)
        # 删除数据库已经有的url
        urls_in_db = (Article
                      .select(Article.url)
                      .where((Article.website == self.website) & (Article.kind == self.kind))
                      .order_by(Article.publish_date.desc())
                      )
        urls_in_db = [x.url for x in urls_in_db]
        index = 0
        for index in range(len(urls)):
            # 数据库中最新的文章url
            if urls[index] in urls_in_db:
                urls = urls[0:index]
                break

        if index == 0:
            logger.info("数据库文章已经最新，无需更新")
            return
        else:
            logger.info(f"新的文章有{len(urls)}篇")

        logger.info("获取列表 {}", len(urls))

        n_articles = len(urls)
        for i, url in enumerate(urls):
            logger.info("({}/{}) 爬取文章: {}", i + 1, n_articles, url)
            time.sleep(0.1)
            article = self.parse_page(url)
            # 文章晚于限定的日期，才保存
            if article.publish_date >= after_date:
                Article.save(article)
            else:
                logger.info(f"当前爬取的文章日期为{article.publish_date},早于限定日期{after_date},爬取结束")
                break