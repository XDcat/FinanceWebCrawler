from controller.article_controller import ArticleController
import typer
app=typer.Typer()

@app.command()
def getLastMonthArticle():
    """
    获取上个月的文章
    :return:
    """
    ArticleController.generate_last_month_articles()


@app.command()
def upDateDatabase(afterDate):
    """
    更新afterDate日期以后的文章，导入数据，afterDate 按照"YY-MM-DD"格式输入
    :param afterDate:
    :return:
    """
    ArticleController.update_db(after_date=afterDate)

@app.command()
def getArticles(start_from , end_at):
    """
    按照指定日期区间展示文章
    :param start_from: 开始时间
    :param end_at: 结束时间
    :return:
    """
    ArticleController.view_article(start_date=start_from, end_date=end_at)


if __name__ == "__main__":
    app()