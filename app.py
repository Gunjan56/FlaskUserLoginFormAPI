from flask import Flask, request, jsonify, url_for, render_template
from flask_migrate import Migrate
from models.model import db, User
from flask_jwt_extended import create_access_token, jwt_required,JWTManager
from flask_mail import Mail,Message
from werkzeug.security import check_password_hash, generate_password_hash
import re
import base64 
import os 
from dotenv import load_dotenv, dotenv_values
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)
JWT = JWTManager(app)
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
    firstname = data['firstname']
    lastname = data['lastname']
    mobileNo = data['mobileNo']
    address = data['address']

    if not re.match(email_Validation, email):
        return jsonify({'message': 'Enter a valid email'}), 400
    
    userDetails = User.query.filter_by(username=username, email=email).first()
    
    if userDetails:
        return jsonify({"message": "User already registered"} )
    
    else:
        user = User(username=username, email=email, password=pass_validate, firstname=firstname, lastname=lastname, mobileNo=mobileNo, address=address)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully',})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
   
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        return jsonify({'access_token': access_token}),200
    else:
        return jsonify({'message': 'Enter valid credentials to login!'}),401
    
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()
    
    if user:
        reset_token = base64.b64encode(email.encode('utf-8')).decode('utf-8')

        send_reset_password_email(email, reset_token)

        return jsonify({'message': 'Reset password link sent to your email'})
    else:
        return jsonify({'message': 'User not found'}), 404

def send_reset_password_email(user_email, reset_token):
    msg = Message('Reset Your Password', sender=os.getenv('MAIL_USERNAME'), recipients=[user_email])
    msg.body = f'Reset your password: {reset_token}'
    mail.send(msg)

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
   
    data = request.get_json()
    new_password = data['new_password']
    confirm_password = data['confirm_password']
    
    if new_password != confirm_password:
        return jsonify({'message': 'New password and confirm password do not match'}), 400
    

    email = base64.b64decode(token).decode('utf-8')
    
    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'message': 'Password reset successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/get/', methods=['GET'])   
@jwt_required() 
def get_user():
    try:
        data = User.query.all()
        return jsonify([user.json() for user in data]), 200
    except:
        return jsonify({'message': 'error getting users'}), 500


@app.route('/user/<int:id>', methods=['GET'])
@jwt_required()
def getUserBy_id(id):
    try:
        data = User.query.filter_by(id=id).first()
        if data:
            return jsonify({'user': data.json()}), 200
        return jsonify({'message': 'User Not Found'}), 404
    except:
        return jsonify({'message': 'Error Getting User'}), 500
    
@app.route('/update/<int:id>', methods=['PUT'])
@jwt_required
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data['email']
      user.password = generate_password_hash(data['password'])
      user.firstname = data['firstname']
      user.lastname = data['lastname']
      user.mobileNo = data['mobileNo']
      user.address = data['address']
      db.session.commit()
      return jsonify({'message': 'User Updated Successfully'}), 200
    return jsonify({'message': 'User Not Found'}), 404
  except:
    return jsonify({'message': 'Error Updating User'}), 500

@app.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return (jsonify({'message': "User Deleted successfully"}), 200)
        return (jsonify({'message': "User Not Found"}), 404)
    except:
        return (jsonify({'message': 'Error while deleting user'}), 500)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
