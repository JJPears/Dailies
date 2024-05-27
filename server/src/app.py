"""
Main application module to start application and load config
"""

import os
from flask import Flask
from dotenv import load_dotenv
from server.src.database import db


load_dotenv()

def create_app(test_config=None):
    """
    Creates and configures an instance of the Flask application.

    :param test_config: Configuration settings for the Flask app during testing.
                        If None, the app will be configured for production.
    :return: An instance of the Flask application.

    This function does the following:
    - Creates a Flask app instance
    - Configures the app from environment variables if test_config is None
    - If test_config is not None, updates the app's configuration with test_config
    - Initializes the mysql database with the app
    """
    dailies_app = Flask(__name__)
    if test_config is None:
        dailies_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
        dailies_app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev',
        )
    else:
        dailies_app.config.update(test_config)

    db.init_app(dailies_app)

    return dailies_app



if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
