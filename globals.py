from flask import Flask, Blueprint

from statics import config

app = Flask("BulletFlask", template_folder="web/build/", static_folder='./web/build', static_url_path='/')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = config.secret_key


cut_objects = {}
