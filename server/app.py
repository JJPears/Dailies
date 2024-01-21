from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from models.models import User
from database import db
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost:3306/dailies'
db.init_app(app)
api = Api(app)

if __name__ == '__main__':
    print('Starting Flask Server')
    with app.app_context():
        print('in app context')
        try:
            db.drop_all()
            db.create_all()
        except Exception as e:
            print("Error creating database:", e)
        print('db created')
        user = User(
            username='test', 
            password='test', 
            email='test@test.com')        
        print("user created:", user)
        db.session.add(user)
        print("user added to session")
        db.session.commit()

        print(User.query.all())

    app.run(debug=True)

