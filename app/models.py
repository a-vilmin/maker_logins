from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    in_lab = db.Column(db.Boolean, default=False)
    visits = db.relationship("Visit", backref='visit')

    def __repr__(self):
        return '<User %r>' % self.username


class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    in_time = db.Column(db.DateTime, unique=True)
    out_time = db.Column(db.DateTime, unique=True)
    purpose = db.Column(db.Text)
    visit_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Purpose %r>' % self.purpose
