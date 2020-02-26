from message.excute.run import create

app,socketio=create()

if __name__ == '__main__':
    socketio.run(app,debug=True)
