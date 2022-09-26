from common.translate import Translator


class Article:
    def __init__(self, publish_date, body, title, url, author, keyword, attachment):
        """
        # 规定爬取的文章存储结构类
        :param publish_date: 出版日期
        :param body: 摘要的html源码
        :param title: 标题
        :param url: 网址
        :param author: 作者
        :param keyword: 关键词
        :param attachment: 附件url
        """
        self.body = body
        self.publish_date = publish_date
        self.title = title
        self.url = url
        self.author = author
        self.keyword = keyword
        self.attachment = attachment
        self.id = None

    @property
    def get_ch_text(self):
        """
        property属性构造
        :param html_code: 正文部分的html源码
        :param appid: 翻译API账号
        :param key: 翻译API密码
        :return: 中文文本
        """
        return Translator.translate(self.body.text, appid='20220914001342952', key='Q_SNAXetAkmZq2yaV4o_')

    def display(self):
        """
        展示所有信息
        :return:
        """
        name = ["body", 'publishdata', 'title', 'url', 'author', 'keyword', 'attachment']
        inform = [self.body, self.publish_date, self.title, self.url, self.author, self.keyword, self.attachment]
        return dict(zip(name, inform))

    def __str__(self):
        res = str(self.display())
        return res
