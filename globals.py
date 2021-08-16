import pymysql
from flask import Flask

from statics import config

app = Flask("BulletFlask", static_folder='public')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = config.secret_key


mysql = pymysql.connect(
    host=config.DB.host,
    port=config.DB.port,
    user=config.DB.user,
    password=config.DB.password,
    db=config.DB.db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)