import datetime


class TimeTransformer:

    @staticmethod
    def strtimeformat(timestring, format='%d %B %Y'):
        """
        时间格式化，统一转换为"YY-MM-DD"
        :param timestring: 时间字符串
        :param format: 输入字符串的格式，比如(23 September 2022)就是'%d %B %Y'，有逗号加上逗号
        :return: 格式化的时间
        """
        time = timestring.strip()
        # 按照相应格式提取信息
        time_format = datetime.datetime.strptime(time, format)
        # 格式化输出
        return time_format.strftime("%Y-%m-%d")
