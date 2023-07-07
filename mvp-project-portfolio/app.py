from flask import Flask, send_from_directory
from models import db
from routes import user_bp, house_bp
from flask_migrate import Migrate
import secrets
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
import os


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:/Users/Adimn/Desktop/frank alx/frank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

@app.route('/static/C:\\Users\\Adimn\\Desktop\\frank alx\\static')
def serve_static(static):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), static)


Session(app)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(house_bp)

with app.app_context():
    from routes import *

if __name__ == '__main__':
    app.run(debug=True)
