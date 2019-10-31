from home import HomeView
from app import app, socketio
HomeView.register(app)
if __name__ == '__main__':
    socketio.run(app)
    app.run(host="localhost", port=9000)
