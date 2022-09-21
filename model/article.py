from bs4 import BeautifulSoup
class Article:
    def __init__(self, publish_date, body, title, url, author, keyword, attachment):
        """
        规定爬取的文章存储结构类
        :param publish_date: 出版日期
        :param body: 摘要的html源码
        :param title: 标题
        :param url: 网址
        :param author: 作者
        :param keyword: 关键词
        :param attachment: 附件url
        :param id: 生成id
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
    def body_txt(self):
        return ""

    def display(self):
        '''
        展示所有信息
        :return:
        '''
        # logging.log(self._body,self._publish_date,self._title,self._url,self._author,self._keyword,self._attachment)
        name = ["body", 'publishdata', 'title', 'url', 'author', 'keyword', 'attachment']
        inform = [self.body, self.publish_date, self.title, self.url, self.author, self.keyword, self.attachment]
        return dict(zip(name, inform))

    def __str__(self):
        res = str(self.display())
        return res
