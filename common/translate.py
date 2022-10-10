import hashlib  # 用来计算MD5码
import random

import requests


class Translator:

    @staticmethod
    def translate(input_text, appid, key):
        """
        翻译模块，调用百度翻译
        :param input_text: 待翻译的文本
        :param appid: APPID，注册后查看
        :param key: 密钥，注册后在控制台查看
        :return:中文文本
        """
        # id，随机数，密钥
        appid, salt, key = appid, f'{random.randint(1, 1e5)}', key
        # 用于验证的签名
        sign = appid + input_text + salt + key
        md5 = hashlib.md5()  # 生成签名计算MD5码
        md5.update(sign.encode('utf-8'))  # 生成签名计算MD5码
        data = {
            "q": input_text,
            "from": "auto",
            "to": "zh",
            "appid": appid,
            "salt": salt,
            "sign": md5.hexdigest()
        }
        # 建立查询
        session = requests.session()
        response = session.post('https://fanyi-api.baidu.com/api/trans/vip/translate', data=data)
        response.encoding = 'utf-8'
        text = response.json()  # 返回的为json格式用json接收数据
        if "error_code" in text.keys():
            print(text)
            raise Exception("翻译API出现问题")
        translated_text = '\n'.join([text['trans_result'][i]['dst'] for i in range(len(text['trans_result']))])


        return translated_text
