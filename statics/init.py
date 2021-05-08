import pymysql

from statics import config as conf


def init_db():
    connection = pymysql.connect(
        host=conf.DB.host,
        port=conf.DB.port,
        user=conf.DB.user,
        password=conf.DB.password
    )

    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % conf.DB.db)
        connection.commit()
        connection.close()

    connection = pymysql.connect(
        host=conf.DB.host,
        port=conf.DB.port,
        user=conf.DB.user,
        password=conf.DB.password,
        db=conf.DB.db
    )
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS `{conf.Instance.user_instance}_users` ("
                       "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                       "username VARCHAR(100),"
                       "email VARCHAR(100),"
                       "password VARCHAR(255),"
                       "is_authenticated TINYINT(1),"
                       "is_active TINYINT(1),"
                       "permissions TEXT,"
                       "groups TEXT"
                       ")")

        cursor.execute(f"CREATE TABLE IF NOT EXISTS `{conf.Instance.instance}_content` ("
                       "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                       "name VARCHAR(255),"
                       "location TEXT,"
                       "type VARCHAR(50),"
                       "permissions TEXT"
                       ")")

        print()
        connection.commit()
        connection.close()

    return True
