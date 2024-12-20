import os 
from flask import Flask
import os

from routers import app_routes
from db_module.db import db

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './empirical-oven-442516-n0-976bfa04c47e.json'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uploads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(app_routes.routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)

