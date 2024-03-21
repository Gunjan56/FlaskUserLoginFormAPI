from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models.model import db, User
import re


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'gunjan'
db.init_app(app) 
migrate = Migrate(app, db)
def validation(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return "valid email"
    else:
        "Invalid Email"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json();
    username = data['username']
    email = data['email']
    password = data['password']
    userDetails = User.query.filter_by(username=username, email=email, password=password).first()

    if userDetails:
        return jsonify({"message": "User already registered"} )
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})


def login():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(username=username, email=email, password=password).first()

    if user:
        return jsonify({'message': "You login successfully!"})
    else:
        return jsonify({'message': 'Enter valid credentials to login!'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
