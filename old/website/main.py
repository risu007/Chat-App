from flask import Flask,jsonify,render_template,url_for,redirect,request,session
from client import Client
from threading import Thread
import time

NAME_KEY= 'name'


app=Flask(__name__)
client=None
app.secret_key= 'rishav'

messages=[]


def disconnect():
    global client
    if client is not None:
        client.disconnect()


@app.route('/login',methods=["POST","GET"])
def login():
    disconnect()
    if request.method=="POST":
        session[NAME_KEY]=request.form["inputName"]
        return redirect(url_for('home'))
    return render_template('login.html',args={"session":session})



@app.route('/logout')
def logout():
    session.pop(NAME_KEY,None)
    return redirect(url_for('login'))



@app.route('/')
@app.route('/home')
def home():

    if NAME_KEY not in session:
        return redirect(url_for('login'))
    global client
    client=Client(session[NAME_KEY])

    return render_template('index.html',args={"login":True,"session":session})



@app.route('/send_messages/',methods=["GET"])
def send_messages(url=None):
    msg=request.args.get("val")
    global client
    if client is not None:
        client.send_messages(msg)
    return "Nothing"


@app.route('/get_messages')
def get_messages():
    return jsonify({"messages":messages})

def update_messages():
    global messages
    run= True
    while run:
        time.sleep(0.1)
        if not client: continue
        new_messages=client.get_messages()
        messages.extend(new_messages)
        for message in new_messages:
            if message=='quit':
                run=False
                break




if __name__=="__main__":
    Thread(target=update_messages).start()
    app.run(debug=True)

