from model.article import Article
from loguru import logger
from common.translate import Translator
from bs4 import BeautifulSoup
from crawler.bis.working_paper import BISWorkingPaperRunner
from crawler.bis.speeches import BISSpeechesRunner
from crawler.ecb.working_paper import ECBWorkingPaperRunner
from crawler.ecb.speeches import ECBSpeechesRunner
from crawler.feds.working_paper.FEDS import FEDSWorkingPaperRunner
from crawler.feds.working_paper.IFDP import IFDPWorkingPaperRunner
from crawler.feds.working_paper.FEDSNOTE import FEDSNOTESWorkingPaperRunner
from crawler.feds.speeches import FEDSpeechesRunner
from crawler.fsb.speeches import FSBSpeechesRunner
from crawler.imf.working_paper import IMFWorkingPaperRunner
from crawler.nebr.working_paper import NEBRWorkingPaperRunner

from utils.ormutils import create_table
import datetime


class DbController:

    @staticmethod
    def translate_db(latest_date=None, overide=False):
        """
        更新数据库中中文html格式文本
        :param latest_date: 指定最新日期
        :param overide: 是否覆盖
        """
        if latest_date is not None:
            articles = (Article
                        .select(Article.aid, Article.title, Article.cn_body, Article.cn_title, Article.body)
                        .where(Article.publish_date > latest_date)
                        .order_by(Article.publish_date.desc())
                        )
        else:
            articles = (Article
                        .select(Article.aid, Article.title, Article.cn_body, Article.cn_title, Article.body)
                        .order_by(Article.publish_date.desc())
                        )

        cnt = 0
        for article in articles:
            # time.sleep(1)
            logger.info(f"总进度 ({cnt}|{len(articles)}) | 正在翻译{article.title}")
            # 传值
            aid = article.aid
            body = article.body
            title = article.title
            cn_body = article.cn_body
            if cn_body == "" and overide == False:
                raise Exception

            # cn_body写过，且不需要重写时
            if cn_body is not None and not overide:
                logger.info("检测到已更新过的中文信息，停止更新")
                break

            special_char = "\\ / : * ? \" \" \' \' < > |".split(" ")
            # 去除title中的特殊字符
            for char in special_char:
                if char in title:
                    title = title.replace(char, "")

            # 更新中文标题
            Article.update(cn_title=Translator.translate(title.strip())).where(Article.aid == aid).execute()

            cn_body = []
            # 处理源码字符串,转换为文本
            if body is not None:
                body = BeautifulSoup(body, "html.parser")

                # 只查找下一级孩子，不需要递归
                if body.div is not None:
                    tag_lst = body.div.find_all(recursive=False)

                elif body.span is not None:
                    tag_lst = body.span.find_all(recursive=False)
                else:
                    raise AttributeError(f"网站html格式不正确")

                for tag in tag_lst:
                    # time.sleep(1)
                    if "h" in tag.name:
                        # 保证输入不为空
                        if tag.text != "":
                            cn_body.append(f"<{tag.name}>{Translator.translate(tag.text)}</{tag.name}>")
                    else:
                        # 删去figure,table的部分
                        if "Figure" not in tag.text:
                            if tag.get('class') is not None:
                                tag_class = tag.get('class')[0]
                                if "table" in tag_class:
                                    continue

                            # 保证输入不为空
                            text = tag.text.strip()
                            if text != "":
                                cn_body.append(f"<{tag.name}>{Translator.translate(text)}</{tag.name}>")
            # 更新中文body
            Article.update(cn_body="\n".join(cn_body)).where(Article.aid == aid).execute()
            cnt += 1

        logger.info(f"共更新{cnt}篇文档的中文信息")

    @staticmethod
    def clear_db(latest_date):
        """
        删除数据库中早于latest_date的久远数据
        :param latest_date: 最新日期
        """
        cnt = len(Article.select().where(Article.publish_date < latest_date))
        Article.delete().where(Article.publish_date < latest_date).execute()

        logger.info(f"成功删除{cnt}条陈旧数据")

    @staticmethod
    def update_db(after_date):
        """
        更新数据库
        :param after_date: 文章的最早日期(必须晚于这个时间)
        :return:
        """
        bisw = BISWorkingPaperRunner()
        biss = BISSpeechesRunner()
        ecbw = ECBWorkingPaperRunner()
        ecbs = ECBSpeechesRunner()
        # 连不上
        fedsw = FEDSWorkingPaperRunner()
        fednotesw = FEDSNOTESWorkingPaperRunner()
        ifdpw = IFDPWorkingPaperRunner()
        feds = FEDSpeechesRunner()
        fsbs = FSBSpeechesRunner()
        imfw = IMFWorkingPaperRunner()
        nebrw = NEBRWorkingPaperRunner()

        try:
            year = datetime.datetime.now().year
            bisw.run(after_date, start_from=1, end_at=3)
            biss.run(after_date, start_from=1, end_at=3)
            ecbw.run(after_date, start_from=year, end_at=year - 1)
            ecbs.run(after_date)
            fedsw.run(after_date, start_from=year, end_at=year - 1)
            fednotesw.run(after_date, start_from=year, end_at=year - 1)
            ifdpw.run(after_date, start_from=year, end_at=year - 1)
            feds.run(after_date)
            fsbs.run(after_date, start_from=1, end_at=3)
            imfw.run(after_date, start_from=1, end_at=2)
            nebrw.run(after_date, start_from=1, end_at=10)
        except ConnectionError as e:
            logger.debug("网站连接失败")
            logger.info(e.__traceback__)

        try:
            DbController.translate_db(latest_date=after_date)
        except Exception as e:
            logger.debug("翻译账号有问题")
