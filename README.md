# main函数指令使用

### def update_database(afterDate):
这个方法用于更新数据库，允许用户指定某个日期after_date,向数据库更新这个日期
以后至今天的所有文章。


### def get_last_month_articles():
这个方法自动获取上个月到现在的文章，并且写入word文档，不需要任何参数。
这个方法包含了上面更新数据库的操作。
比如update_database("2022-10-01")，就会查询所有网站该日期后发表的文章，
导入数据库，并且通过viewer模块生成word。

### def get_articles(start_from, end_at):
这个方法是上个方法的扩展，允许指定时间范围，获取对应文章的word文档。
比如get_articles(”2022-01-01“, ”2022-09-30“)可以获取这两个时间段的所有网站文章的word文档。
已经存在的word文档不会重写。



