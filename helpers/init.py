import sys

import pymysql

from helpers import db
from statics import config as conf


def init_db():
    try:
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
    except:
        print("Could not autocreate database! Aborting startup!")
        sys.exit(1)

    db.Base.metadata.create_all(db.engine)

    return True
