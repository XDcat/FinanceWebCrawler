import peewee
from view.viewer import ArticleViewer
from model.article import Article
import datetime
from common.timetransformer import TimeTransformer


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
    def fetch_last_month_articles():
        now = datetime.datetime.now()
        start_month = now.month
        start_year = now.year
        now = now.strftime("%Y-%m-%d")
        if start_month == 1:
            start_year -= 1
            start_month = 12
        else:
            start_month -= 1
        start_timestamp = f"{start_year} {start_month} 1"
        start_timestamp = TimeTransformer.strtimeformat(start_timestamp, "%Y %m %d")
        articles_tup = ArticleController.select_arts_from_db(start_timestamp, now)
        return articles_tup

    @staticmethod
    def fetch_article(start_date, end_date):

        articles_tup = ArticleController.select_arts_from_db(start_date, end_date)
        for article in articles_tup:
            ar = ArticleViewer(article)
            ar.publish_en_report()
