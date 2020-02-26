from flask import Flask, render_template, url_for,session,redirect,request,jsonify,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=False)
app.config['SECRET_KEY']='97881300a80684fbe6104db067ce9594'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)



@app.before_first_request
def create_tables():
    db.create_all()

def create_app():

    return app
