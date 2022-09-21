import unittest
import warnings

from extract_information_from_page import ExtractInfFromPage
from extract_page_from_guidelist import DetectGuideList
from translate import Translator

warnings.simplefilter("ignore", ResourceWarning)


class MyTestCase(unittest.TestCase):
    def test_mylogger(self):
        # self.assertEqual(True, False) # add assertion here
        pass

    def test_testlog(self):
        pass

    def test_DetectGuideList(self):
        url = r"https://www.bis.org/wpapers/index.htm?m=1026"
        rec=DetectGuideList.readPagefromList(url)
        return rec

    def test_Extract_inform_from_page(self):
        url='https://www.bis.org/publ/work1038.htm'
        ExtractInfFromPage.extractMessagefromArticle(url)
        return

    def test_translate(self):
        text="ExtractInfFromPage.extractMessagefromArticle(url) ResourceWarning: Enable tracemalloc to get the object allocation traceback"
        ch_text=Translator.translate(text,appid='20220914001342952',key='Q_SNAXetAkmZq2yaV4o_')
        print(ch_text)



if __name__ == '__main__':
    unittest.main()

