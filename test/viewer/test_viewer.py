import unittest
from view.viewer import *
from controller.article_controller import ArticleController


class MyTestCase(unittest.TestCase):

    def test_href(self):
        document = docx.Document()
        p = document.add_paragraph()

        # add a hyperlink with the normal formatting (blue underline)
        hyperlink = add_hyperlink(p, 'http://www.google.com', 'Google', None, True)

        # add a hyperlink with a custom color and no underline
        hyperlink = add_hyperlink(p, 'http://www.google.com', 'Google', 'FF8822', False)

        document.save(r"E:\crawler\FinanceWebCrawler\results\test.docx")

    def test_viewer(self):
        arts = ArticleController.select_arts_from_db("2022-09-01", "2022-09-30","ECB")
        for art in arts:
            vw = ArticleViewer(art)

            vw.publish_en_report()

    def test_cn_viewer(self):
        arts = ArticleController.select_arts_from_db("2022-09-01", "2022-09-30")
        dic=dict()
        for art in arts:
            name = art.website + art.kind
            if dic.get(name,0)<1:
                dic[name]=0
                vw = ArticleViewer(art)
                dic[name]+=1
                vw.publish_cn_report()

    def test_char(self):
        special_char = r"\ / : * ? " " < > |".split(" ")
        print(special_char)
