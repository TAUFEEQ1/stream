from home import HomeView
from . import app, socketio
HomeView.register(app)
if __name__ == '__main__':
    socketio.run(app)
    app.run()
