import pymysql

# 讓 pymysql 偽裝成 Django 預設的 MySQLdb
pymysql.install_as_MySQLdb()