
from crawler.base_runner import BaseRunner
class ECBWorkingPaperRunner(BaseRunner):
    def __init__(self):
        super(ECBWorkingPaperRunner, self).__init__(
            "ECB working papers",
            "https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html"
        )

    def get_page_num(self):
        # TODO: exmpale
        pass

    def get_one_list(self, page: int):
        # TODO: exmpale
        pass

    def parse_page(self, url):
        # TODO: exmpale
        pass