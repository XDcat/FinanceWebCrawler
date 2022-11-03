from controller.article_controller import ArticleController
from controller.db_controller import DbController
import typer

app = typer.Typer()


@app.command()
def get_last_month_articles():
    """
    获取上个月的文章
    """
    ArticleController.generate_last_month_articles()


@app.command()
def update_database(after_date):
    """
    更新afterDate日期以后的文章，导入数据，afterDate 按照"YY-MM-DD"格式输入
    """
    DbController.update_db(after_date=after_date)


@app.command()
def get_articles(start_from, end_at):
    """
    按照指定日期区间生成文章
    :param start_from: 开始时间
    :param end_at: 结束时间
    """
    ArticleController.view_article(start_date=start_from, end_date=end_at)


if __name__ == "__main__":
    app()
