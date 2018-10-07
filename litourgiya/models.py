from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}'


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    season = db.Column(db.String(80), nullable=False)
    season_week = db.Column(db.Integer, nullable=False)
    weekday = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('calendars', lazy=True))

    def __repr__(self):
        return f'<Calendar {self.date}>'


class Celebration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    colour = db.Column(db.String(80), nullable=False)
    rank = db.Column(db.String(80), nullable=False)
    rank_num = db.Column(db.Float, nullable=False)

    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'), nullable=False)
    calendar = db.relationship('Calendar', backref=db.backref('celebrations', lazy=True))

    def __repr__(self):
        return f'<Celebration {self.title}>'
