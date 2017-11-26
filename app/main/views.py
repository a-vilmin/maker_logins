from flask import current_app, render_template, redirect, \
    url_for, request, abort
from flask_login import current_user, login_required
from datetime import datetime
from . import main
from .forms import VisitForm
from ..models import Visit, User
from .. import db


@main.route('/', methods=['GET', 'POST'])
@main.route('/index')
def index():
    all_users = User.query.filter_by(in_lab=True)
    if not all_users:
        print("thats the problem")
    return render_template('index.html', users=all_users)


@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form = VisitForm()
    user = current_user._get_current_object()

    if user.username != username:
        abort(500)
    if form.validate_on_submit():
        visit = Visit(purpose=form.purpose.data,
                      visit_user=user.id,
                      in_time=datetime.now(),
                      type_visit=form.type_visit.data)

        db.session.add(visit)
        db.session.commit()
        return redirect(url_for('main.user', username=username))
    return render_template('user.html', user=user, form=form)


@main.route('/log_visit/<username>', methods=['GET', 'POST'])
@login_required
def log_visit(username):
    form = VisitForm()
    user = current_user._get_current_object()

    if user.username != username:
        abort(500)
    if form.validate_on_submit():
        visit = Visit(purpose=form.purpose.data,
                      visit_user=user.id,
                      in_time=datetime.now(),
                      type_visit=form.type_visit.data)

        db.session.add(visit)
        db.session.commit()
        return redirect(url_for('main.user', username=username))
    return render_template('log_visit.html', user=user, form=form)
