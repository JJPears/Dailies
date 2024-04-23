"""
Main application module to start application and load config
"""

import os
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from server.database import db


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
db.init_app(app)
api = Api(app)

if __name__ == "__main__":
    app.run(debug=True)
