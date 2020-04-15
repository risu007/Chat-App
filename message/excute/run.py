from flask_socketio import SocketIO
from message.new import create_app
from flask import session

app=create_app()
socketio = SocketIO(app)

from message.new.models import Chat,User
from message.new import db
from message.new.main import view

app.register_blueprint(view, url_prefix="/")


@socketio.on('my event')
def handle_my_custom_event(json,methods=["POST,GET"]):
    data=dict(json)
    if "name" in data:
        id=User.query.filter_by(username=data["name"]).first().id
        chat=Chat(user_id=id,msg=data["msg"],date_msg=data["time"])
        db.session.add(chat)
        db.session.commit()
    socketio.emit('message pass',json)


# disconnect during network failure or close tab
# @socketio.on('disconnect')
# def test_disconnect():
#     if 'name' in session:
#         print('disconnect- ',session['name'])
#         name=session['name']
#         session.pop('name',None)
#         session.modified=True
#         socketio.emit('message pass',{'msg': 'Disconnected!','connect':'disconnect','name':name})



def create():
    return (app,socketio)


