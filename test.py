import unittest
import warnings
from common.Logger import logger

from extract_information_from_page import ExtractInfFromPage
from extract_page_from_guidelist import DetectGuideList
from translate import Translator


# warnings.simplefilter("ignore", ResourceWarning)


class MyTestCase(unittest.TestCase):
    def test_logger(self):
        # self.assertEqual(True, False) # add assertion here
        logger.info("Hello world")

    def test_detect_guide_list(self):
        url = r"https://www.bis.org/wpapers/index.htm?m=1026"
        rec = DetectGuideList.read_page_from_list(url)
        logger.info(rec)
        

    def test_extract_inform_from_page(self):
        url = 'https://www.bis.org/publ/work1038.htm'
        res = ExtractInfFromPage.extract_message_from_article(url)
        logger.info(res)
        
        logger.info("body text \n{}", res.body_txt)
        
        

    def test_translate(self):
        text = "ExtractInfFromPage.extractMessagefromArticle(url) ResourceWarning: Enable tracemalloc to get the object allocation traceback"
        ch_text = Translator.translate(text, appid='20220914001342952', key='Q_SNAXetAkmZq2yaV4o_')
        logger.info(ch_text)