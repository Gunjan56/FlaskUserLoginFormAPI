from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models.model import db, User
from werkzeug.security import check_password_hash, generate_password_hash
import re
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'gunjan'
db.init_app(app) 
migrate = Migrate(app, db)

email_Validation = r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json();
    username = data['username']
    email = data['email']
    password = data['password']
    pass_validate = generate_password_hash(password)

    if not re.match(email_Validation, email):
        return jsonify({'message': 'Enter a valid email'}), 400
    
    userDetails = User.query.filter_by(username=username, email=email, password=password).first()
    
    
    
    if userDetails:
        return jsonify({"message": "User already registered"} )
    
    else:
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

    if user and check_password_hash(user.password, password):
        return jsonify({'message': "You login successfully!"})
    else:
        return jsonify({'message': 'Enter valid credentials to login!'})
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
