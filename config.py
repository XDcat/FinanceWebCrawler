import peewee
import os

db_path = os.path.join(os.path.dirname(__file__), "database/FinanceWebCrawler.db")
report_prefix_path = os.path.join(os.path.dirname(__file__), "results/")
db = peewee.SqliteDatabase(db_path)

# 黄艺
# appid = "20221021001405753"
# password = "ftUGnN0S4VdrI3HbRQq9"

# 曾连杰
appid = "20191016000342020"
password = "FERT7SoJhp0WagCy2Gz3"

# 邹宗霖
# appid = "20220914001342952"
# password = "Q_SNAXetAkmZq2yaV4o_"