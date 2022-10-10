from controller.article_controller import ArticleController
from view.viewer import ArticleViewer

def main():
    arts = ArticleController.select_arts_from_db("2022-09-01", "2022-09-30")
    for art in arts:
        vw = ArticleViewer(art)
        vw.publish_en_report()



if __name__ == '__main__':
    main()