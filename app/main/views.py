from flask import current_app, render_template
from . import main


@main.route('/', methods=['GET', 'POST'])
@main.route('/index')
def index():
    return render_template('index.html')
