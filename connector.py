import requests as rq


class Connector:
    def __init__(self):
        pass

    @staticmethod
    def connectToUrl(url, encoding='utf-8', method="get", data=None, params=None):
        '''
        连接到网站
        :param url: 网站
        :param encoding: 编码方式
        :param method: 连接请求类型，可选get/post
        :param data: 传送的数据 post专用
        :return: 网页响应response
        '''
        if method == 'post' and data is None:
            raise Exception
        # 建立查询
        session = rq.session()
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
        session.headers = header
        if params is None:
            if method == "get":
                response = session.get(url)
                response.encoding = encoding
                return response
            else:
                response = session.post(url, data=data)
                response.encoding = encoding
                return response
        else:
            if method == "get":
                response = session.get(url, params=params)
                response.encoding = encoding
                return response
            else:
                response = session.post(url, params=params, data=data)
                response.encoding = encoding
                return response
