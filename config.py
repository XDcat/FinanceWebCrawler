import peewee
import os

db_path = os.path.join(os.path.dirname(__file__), "database/FinanceWebCrawler.db")
report_prefix_path = os.path.join(os.path.dirname(__file__), "results/")
db = peewee.SqliteDatabase(db_path)
appid = "20191016000342020"
password = "FERT7SoJhp0WagCy2Gz3"
