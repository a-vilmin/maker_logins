from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    in_lab = db.Column(db.Boolean, default=False)
    visits = db.relationship("Visit", backref='visit')
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    in_time = db.Column(db.DateTime, unique=True)
    out_time = db.Column(db.DateTime, unique=True)
    purpose = db.Column(db.Text)
    visit_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Purpose %r>' % self.purpose
