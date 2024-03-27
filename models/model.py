from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    mobileNo = db.Column(db.String(15))
    address = db.Column(db.String(100))
    reset_password_token = db.Column(db.String(100), unique=True)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'firstname': self.firstname, 'lastname': self.lastname, 'mobileNo': self.mobileNo, 'address': self.address}
