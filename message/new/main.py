from flask import Flask, render_template, url_for,session,redirect,request,jsonify,flash,Blueprint

from flask_sqlalchemy import SQLAlchemy
from message.new import db
from message.new.models import User,Chat
from datetime import datetime
import pytz


NAME_KEY= 'name'

view = Blueprint("views", __name__)
from message.excute.run import socketio

@view.route('/home')
@view.route('/')
def home():
    if NAME_KEY not in session:
        return redirect(url_for('views.login'))
    print('in home- ',session['name'])
    return render_template('index.html')

@view.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        name=request.form["input_name"]
        user=User.query.filter_by(username=name).first()
        if user==None:
            db.session.add(User(username=name))
            db.session.commit()
            session[NAME_KEY]=name
            flash(f'You are successfully logged in as {session[NAME_KEY]}')
            return redirect(url_for('views.home'))
        else:
            flash('Username is taken.Please use another name!')
    return render_template('login.html')

@view.route('/logout')
def logout():
    name=session[NAME_KEY]
    session.pop(NAME_KEY,None)
    session.modified=True
    flash(f'You are successfully logged out')
    t=datetime.now(pytz.timezone('Asia/Kolkata'))
    t=t.strftime('%d-%m-%Y %H:%M:%S')
    socketio.emit('left',{'name':name,'msg':' left the chat!!!','time':t})
    return redirect(url_for('views.login'))


@view.route('/get_name')
def get_name():
    user={"name":""}
    if NAME_KEY  in session:
        user={"name":session[NAME_KEY]}
    return jsonify(user)






