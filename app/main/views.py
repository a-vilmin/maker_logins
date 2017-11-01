from flask import current_app, render_template, redirect, url_for, request, abort
from flask_login import current_user
from datetime import datetime
from . import main
from .forms import VisitForm
from ..models import Visit
from .. import db


@main.route('/', methods=['GET', 'POST'])
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    form = VisitForm()
    user = current_user._get_current_object()

    if user.username != username:
        abort(500)
    if form.validate_on_submit():
        visit = Visit(purpose=form.purpose.data,
                      visit_user=user.id,
                      in_time=datetime.now())
        db.session.add(visit)
        db.session.commit()
        return redirect(url_for('main.user', username=username))
    return render_template('user.html', user=user, form=form)


@main.before_app_request
def before_request():
    if not current_user.is_authenticated \
            and request.endpoint != 'static' \
            and 'user' in request.endpoint:
        return redirect(url_for('main.index'))
