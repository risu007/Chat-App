from message.new import db


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    chats=db.relationship('Chat',backref='author',lazy=True)


class Chat(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    msg=db.Column(db.Text,nullable=False)
    date_msg=db.Column(db.String(100),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)


