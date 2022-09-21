import logging
from logging.handlers import RotatingFileHandler

class MyLogger:

    def __init__(self):
        self._name="log.log"
        self._logger = logging.getLogger('logger')
        self._logger.setLevel(logging.INFO)
        rotating_handler = logging.handlers.RotatingFileHandler(self._name, encoding='UTF-8',
                                                                maxBytes=1024 * 1024, backupCount=2)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        rotating_handler.setFormatter(formatter)
        self._logger.addHandler(rotating_handler)

    def writeIntoLog(self,information):
        '''
        写入信息
        :param information:操作信息，字符串输入
        :return:
        '''
        self._logger.info(information)


if __name__=='__main__':
    mylogger=MyLogger()
    mylogger.writeIntoLog('whathappened?')
    mylogger.writeIntoLog('whathappened?')
    mylogger.writeIntoLog('whathappened?')