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

        logger.info(f"reading articels of {year} now,totally {1996}~{datetime.datetime.now().year} in all.")

        guide_url=f"https://www.federalreserve.gov/econres/feds/{year}.htm"

        response = self.session.get(guide_url)

        html = BeautifulSoup(response.content, "html.parser")

        # 查找htm数据的网址
        htm_url = html.find('div', class_="bisobj_document_list").get('data-document_list_url')

        pagenums = self.get_page_num()

        urls = []
        logger.info(f"reading page of year {year} now,totally {pagenums} in all.")

        response1.encoding = 'utf-8'
        article_list = BeautifulSoup(response1.content, "html.parser")
        article_url_list = article_list.find_all("div", class_='title')
        # 构建指向page的网址
        pre = 'https://www.bis.org'
        for html_label in article_url_list:
            href = html_label.find('a').get('href')
            urls.append(pre + href)
        logger.info(f"get urls successfully,url={self.home_url}, get {len(urls)} urls in all.")
        return urls


        # 构建指向page的网址
        return [htm_url]

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
        # 这个page集合了一整年的文章，但是html结构规整，分成两块
        part1 = data.find("dt")
        part2 = part1.next_sibling
        pagenums = (len(list(part1.next_siblings)) + 1) // 2
        logger.info(f"reading {url} now,get {pagenums} articles in all.")
        count = 1
        while count <= pagenums:
            logger.info(f"reading number {count} article now,have {pagenums} articles in all!")
            # 获取出版日期
            publish_date = part1.text
            # 拿到标题
            title = part2.select('div[class=title]')[0].text
            # 拿到附件
            attachment_url = "https://www.ecb.europa.eu/" + part2.select('div[class=title]')[0].find("a").get("href")
            # 拿到作者
            authors = part2.find("div", class_="authors").text
            # 拿到正文html
            body = part2.find("div", class_="content-box")
            # keywords网站中并没有，需要到attachment中的pdf查看
            keywords = None
            # url就是某年份的页面
            art_url = url
            # 存储到结构体
            saved_data = Article(publish_date, body, title, art_url, authors, keywords, attachment_url)
            # todo 保存到数据库，发现重复的就可以停止函数
            # logger.info(saved_data.display())
            # 更新part1,part2
            part1 = part2.next_sibling
            if part1 is None:
                break
            part2 = part1.next_sibling
            if part2 is None:
                break
            count += 1
            logger.info("get  article information successfully")
        return saved_data

    def get_list(self, start_from=1999):
        total_page_num = self.get_page_num()
        res = []
        for i in range(start_from, start_from+total_page_num ):
            res.extend(self.get_one_list(i))
        return res
