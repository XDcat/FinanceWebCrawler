import requests
from bs4 import BeautifulSoup
from crawler.base_runner import BaseRunner
from common.Logger import logger
from model.article import Article


class IMFSpeechesRunner(BaseRunner):
    def __init__(self):
        super(IMFSpeechesRunner, self).__init__(
            "IMF speeches",
            "https://www.imf.org/en/news/searchnews#sort=%40imfdate%20descending"
        )

    def get_page_num(self):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对IMFSPEECH网站
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """

        return 100

    def get_one_list(self, page_num):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """
        # 建立查询
        guide_url = f"https://www.imf.org/en/news/searchnews#first={page_num * 10 - 10}&sort=%40imfdate%20descending"
        response = self.session
        response.encoding = 'utf-8'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.3161 SLBChan/25'}
        response.headers = header
        response = response.get(guide_url)

        data = BeautifulSoup(response.content, "html.parser")
        pagenums = self.get_page_num()
        logger.info(f"reading page{page_num} now,totally {pagenums} in all.")
        # 访问htm数据，这也是个html,采用post方法,将参数传给body
        # 嵌套拿取网址
        print(data)
        return

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

        # 拿到keywords
        keywords = data.find("meta", attrs={"name": "Keywords"})
        if keywords is not None:
            keywords = keywords.get("content")

        # 拿到附件
        if len(data.select("section p[class=pub-desc] a")) > 0:
            attachment_url1 = data.select("section p[class=pub-desc] a")[0]
        else:
            attachment_url1 = None

        if attachment_url1 is None:
            attachment_url2 = data.find("a", class_="piwik_download").get("href")
            if attachment_url2 is None:
                raise Exception("url not found")
            else:
                attachment_url = attachment_url2.get("content")
        else:
            attachment_url = attachment_url1.get("href")
        # 合并
        attachment_url = "https://www.imf.org" + attachment_url
        # 存储到结构体
        saved_data = Article(publish_date, body, title, art_url, authors, keywords, attachment_url)
        logger.info(saved_data.display())
        # 中文文本
        # ch_text = saved_data.get_ch_text
        logger.info("get temp article information successfully")
        return saved_data

