from flask import Flask, request, jsonify, url_for, render_template
from flask_migrate import Migrate
from models.model import db, User
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity,JWTManager
from flask_mail import Mail,Message
from werkzeug.security import check_password_hash, generate_password_hash
import re
import secrets
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'gunjan'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'xyz@gmail.com'
app.config['MAIL_PASSWORD'] = 'xyz'
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
        token = secrets.token_urlsafe(32)
        user.reset_password_token = token
        db.session.commit()

        reset_link = url_for('reset_password', token=token, _external=True)
        send_reset_password_email(email, reset_link)

        return jsonify({'message': 'Reset password link sent to your email'})
    else:
        return jsonify({'message': 'User not found'}), 404

def send_reset_password_email(user_email, reset_link):
    msg = Message('Reset Your Password', sender='xyz@gmail.com', recipients=[user_email])
    msg.body = f'Reset your password: {reset_link}'
    mail.send(msg)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        return render_template('reset_password.html', token=token)

    if request.method == 'POST':
        data = request.get_json()
        new_password = data['password']
        user = User.query.filter_by(reset_password_token=token).first()

        if user:
            user.password = generate_password_hash(new_password)
            user.reset_password_token = None
            db.session.commit()
            return jsonify({'message': 'Password reset successfully'}), 200
        else:
            return jsonify({'message': 'Invalid or expired token'}), 400

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
