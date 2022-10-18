from crawler.base_runner import BaseRunner
import datetime
from bs4 import BeautifulSoup
from common.Logger import *
from model.article import Article
import json
from common.timetransformer import TimeTransformer


class FEDSpeechesRunner(BaseRunner):
    def __init__(self):
        super(FEDSpeechesRunner, self).__init__(
            website="FED",
            kind="speech",
            home_url="https://www.federalreserve.gov/newsevents/speeches.htm"
        )

    def get_page_num(self):
        """
        FED SPEECHES
        :param url:导航页面的Url
        :return: 所有Page页面的url
        """

        return 1

    def get_one_list(self, page_num):
        """
        从List页面寻找到Page页面的URL,直接找htm,针对FED SPEECH网站
        :param page_num:导航页面的Url
        :return: 所有Page页面的url
        """

        guide_url = "https://www.federalreserve.gov/json/ne-speeches.json"

        response = self.session.get(guide_url)
        # 去除BOM
        decoded_data = response.text.encode().decode('utf-8-sig')
        data = json.loads(decoded_data)
        logger.info(data[0])
        urls = []
        pre = "https://www.federalreserve.gov"
        cnt = 100
        for info in data:
            if info.get("l") is not None:
                urls.append(pre + info.get("l"))
                cnt -= 1
            if cnt == 0:
                break

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
        title = data.select("h3[class=title]")
        if len(title) > 0:
            title = title[0].text.strip()
        # 拿到正文html源码
        body = data.select("div[id=article]>div[class='col-xs-12 col-sm-8 col-md-8']")
        # 有文章没有Summary，直接空着了
        if len(body) > 0:
            paras = body[0].find_all("p",recursive=False)

            body_list=[]
            for para in paras:
                # 识别strong内的子标题
                if para.strong is not None:
                    subtitle=para.strong.text.strip()
                    body_list.append(f"<h3>{subtitle}</h3>")
                    body_list.append("<p>"+para.text.replace(subtitle,"", 1).strip()+"</p>")
                else:
                    body_list.append(str(para))


            body = "<div>" + "\n".join(body_list) + "</div>"
        else:
            body = None

        # 拿到url
        art_url = url

        # 作者
        authors = data.select("p[class=speaker]")
        if len(authors) > 0:
            authors = authors[0].text.strip()

        # 日期的class标签都是pub-desc hide
        publish_date = data.select("p[class='article__time']")
        if len(publish_date) > 0:
            publish_date = publish_date[0].text
            publish_date = TimeTransformer.strtimeformat(publish_date, "%B %d, %Y")
        else:
            publish_date = None

        # 拿到keywords,该网站并没有
        keywords = None

        # 附件
        pre = "https://www.federalreserve.gov"
        attachment_url = data.select("div[class=shareDL]>a")
        if len(attachment_url) > 0:
            attachment_url = pre + attachment_url[0].get("href")
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
