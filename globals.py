from flask import Flask

from statics import config

app = Flask("BulletFlask", static_folder='public')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = config.secret_key

cut_objects = {}
