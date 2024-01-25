from flask import Flask
from flask_restful import Api
from models.models import User
from database import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db.init_app(app)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)

