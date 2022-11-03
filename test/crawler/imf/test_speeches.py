from unittest import TestCase
from crawler.imf.speeches import IMFSpeechesRunner
from common.Logger import logger
import requests


class TestWorkingPaper(TestCase):
    def setUp(self) -> None:
        self.runner = IMFSpeechesRunner()

    def test_run(self):
        url = "https://www.imf.org/coveo/rest/v2?sitecoreItemUri=sitecore%3A%2F%2Fweb%2F%7B5ABCDAEC-30A6-4F1B-835C-5D1AB8F77FB5%7D%3Flang%3Den%26amp%3Bver%3D2&siteName=imf"
        se = requests.session()
        res=se.get(url)
        print(res.json())

