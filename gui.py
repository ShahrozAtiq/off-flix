from flaskwebgui import FlaskUI 
from app import app
ui = FlaskUI(app, width=1280, height=720, start_server='flask',)


if __name__ == "__main__":
    ui.run()