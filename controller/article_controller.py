import peewee
from view.viewer import ArticleViewer
from model.article import Article
import datetime
from common.Logger import logger
from common.timetransformer import TimeTransformer
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


class ArticleController:

    @staticmethod
    def select_arts_from_db(start_date=None, end_date=None, website=None, kind=None):

        condition_lst = []
        if start_date is not None:
            condition_lst.append("(Article.publish_date >= start_date)")
        if end_date is not None:
            condition_lst.append("(Article.publish_date<=end_date)")
        if website is not None:
            condition_lst.append("(Article.website==website)")
        if kind is not None:
            condition_lst.append("(Article.kind==kind)")

        where_condition = eval("&".join(condition_lst))

        articles = (Article
                    .select()
                    .where(where_condition)
                    .order_by(Article.publish_date)
                    )
        return tuple(articles)

    @staticmethod
    def generate_last_month_articles():
        now = datetime.datetime.now()
        start_month = now.month
        start_year = now.year
        # now = now.strftime("%Y-%m-%d")
        if start_month == 1:
            start_year -= 1
            start_month = 12
        else:
            start_month -= 1
        start_timestamp = f"{start_year} {start_month} 1"
        start_timestamp = TimeTransformer.strtimeformat(start_timestamp, "%Y %m %d")
        # 更新数据库
        try:
            ArticleController.update_db(after_date=start_timestamp)
        except ConnectionError as e:
            logger.info(e.__traceback__)
            logger.debug("网站链接失败，请过段时间重试")
        articles_tup = ArticleController.select_arts_from_db(start_date=start_timestamp)
        for art in articles_tup:
            vw = ArticleViewer(art)

            vw.publish_en_report()

    @staticmethod
    def view_article(start_date, end_date):

        articles_tup = ArticleController.select_arts_from_db(start_date, end_date)
        for article in articles_tup:
            vw = ArticleViewer(article)

            vw.publish_en_report()

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
