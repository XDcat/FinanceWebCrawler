#规定爬取的文章存储结构类
class ArticleStructure:
    def __init__(self,publish_date,body,title,url,author,keyword,attachment):
        '''
        初始化方法
        :param publish_date: 出版日期
        :param body: 摘要的html源码
        :param title: 标题
        :param url: 网址
        :param author: 作者
        :param keyword: 关键词
        :param attachment: 附件url
        '''
        self._body=body
        self._publish_date=publish_date
        self._title=title
        self._url=url
        self._author=author
        self._keyword=keyword
        self._attachment=attachment

    def getBody(self):
        '''
        获取文章的出版日期
        :return:
        '''
        return self._publish_date

    def getMainText(self):
        '''
        获取正文源码
        :return:
        '''
        return self._body

    def getTitle(self):
        '''
        获取文章的标题
        :return:
        '''
        return self._title

    def getUrl(self):
        '''
        获取文章url
        :return:
        '''
        return self._url

    def getAuthor(self):
        '''
        获取作者信息
        :return:
        '''
        return self._author

    def getKeyword(self):
        '''
        获取关键词
        :return:
        '''
        return self._keyword

    def getPdf(self):
        '''
        获取正文pdf
        :return:
        '''
        return self._attachment

    def describe(self):
        '''
        展示所有信息
        :return:
        '''
        # logging.log(self._body,self._publish_date,self._title,self._url,self._author,self._keyword,self._attachment)
        name=["body",'publishdata','title','url','author','keyword','attachment']
        inform=[self._body,self._publish_date,self._title,self._url,self._author,self._keyword,self._attachment]
        return dict(zip(name,inform))

