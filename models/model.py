from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False, unique=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    mobileNo = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email, 
                'firstname': self.firstname, 'lastname': self.lastname, 'mobileNo': self.mobileNo, 'address': self.address}