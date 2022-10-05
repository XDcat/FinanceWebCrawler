# 创建表
def create_table(table):
    if not table.table_exists():
        table.create_table()


# 删除表
def drop_table(table):
    if table.table_exists():
        table.drop_table()

