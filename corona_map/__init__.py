from flask import Flask
from . import models, views, data

app = Flask(__name__)
#app.config.from_pyfile('config.py')
app.config.from_json('config.json')
print('Config: ', app.config['TITLE'])
views.init_app(app)
data.init_app(app)




