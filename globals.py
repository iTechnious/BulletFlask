import mysql.connector.cursor
from flask import Flask
from dbutils.pooled_db import PooledDB

from statics import config

app = Flask("BulletFlask", static_folder='public')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = config.secret_key

"""
pymysql.threadsafety = 3

mysql = pymysql.connect(
    host=config.DB.host,
    port=config.DB.port,
    user=config.DB.user,
    password=config.DB.password,
    db=config.DB.db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
"""

connection_pool = PooledDB(mysql.connector, 5,
                           host=config.DB.host,
                           port=config.DB.port,
                           user=config.DB.user,
                           password=config.DB.password,
                           db=config.DB.db,
                           buffered=True
                           )

connection_pool.connection().cursor().execute("SET NAMES utf8mb4")
