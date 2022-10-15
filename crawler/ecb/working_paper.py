from crawler.base_runner import BaseRunner
import datetime
from bs4 import BeautifulSoup
from common.Logger import *
from model.article import Article
from utils.ormutils import create_table
from common.timetransformer import TimeTransformer


class ECBWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(ECBWorkingPaperRunner, self).__init__(
            website="ECB",
            kind="working_paper",
            home_url="https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html"
        )

    def get_page_num(self):
        """
        ecb按照年份分，最早的是1999
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """
        new_year = datetime.datetime.now().year
        old_year = 1999
        return new_year - old_year + 1

    def get_one_list(self, year):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对BIS网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """

        # 访问htm数据，这也是个html,采用post方法,将参数传给body
        htm_url = f"https://www.ecb.europa.eu/pub/research/working-papers/html/papers-{year}.include.en.html"
        # 嵌套拿取网址
        # pagenums = self.get_page_num()

        logger.info(f"reading articels of {year} now,totally {1999}~{datetime.datetime.now().year} in all.")

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
            publish_date = TimeTransformer.strtimeformat(publish_date, "%d %B %Y")
            # 拿到标题
            title = part2.select('div[class=title]')[0].text
            # 拿到附件
            attachment_url = "https://www.ecb.europa.eu/" + part2.select('div[class=title]')[0].find("a").get("href")
            # 拿到作者
            authors = part2.find("div", class_="authors")
            authors_list = authors.ul.find_all(recursive=False)
            authors = ", ".join([tag.text.strip() for tag in authors_list])

            # 拿到正文html
            body = part2.find("div", class_="content-box")
            body = "<div>" + "\n".join(list(map(str, body.dl.find_all(recursive=False)))[:-2]) + "</div>"
            # keywords网站中并没有，需要到attachment中的pdf查看
            keywords = None
            # url就是某年份的页面
            art_url = url
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
            saved_data.save()
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

    def get_list(self, start_from=1999, end_at=None):
        if end_at is None:
            end_at = self.get_page_num() + start_from
        res = []
        for i in range(start_from, end_at):
            res.extend(self.get_one_list(i))
        return res

    def run(self, start_from=1999, end_at=None):
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
            self.parse_page(url)
