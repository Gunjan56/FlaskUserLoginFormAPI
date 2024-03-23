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
   

    user = User.query.filter_by(email=email, password=password).first()

    if user and check_password_hash(user.password, password):
        return jsonify({'message': "You login successfully!"})
    else:
        return jsonify({'message': 'Enter valid credentials to login!'})
    
@app.route('/get/', methods=['GET'])    
def get_user():
    try:
        data = User.query.all()
        return jsonify([user.json() for user in data]), 200
    except:
        return jsonify({'message': 'error getting users'}), 500


@app.route('/user/<int:id>', methods=['GET'])
def getUserBy_id(id):
    try:
        data = User.query.filter_by(id=id).first()
        if data:
            return jsonify({'user': data.json()}), 200
        return jsonify({'message': 'User Not Found'}), 404
    except:
        return jsonify({'message': 'Error Getting User'}), 500
    
@app.route('/update/<int:id>', methods=['PUT'])
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
    # with app.app_context():
        # db.create_all()
    app.run(debug=True, port=8000)
