from flask import Blueprint, render_template, current_app

mod = Blueprint('/', __name__)

@mod.route('/')
def index():
    title = current_app.config['TITLE']
    regions = current_app.config['REGIONS']
    print('title: ', title)
    print('Regions: ', regions)
    return render_template('dashboard.html', TITLE=title, REGIONS=regions)