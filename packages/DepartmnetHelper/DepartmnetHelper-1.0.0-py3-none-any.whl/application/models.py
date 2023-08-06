from application import db
from flask_login import UserMixin

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    salary =  db.Column(db.Integer, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
   
    department_ref = db.Column(db.Integer, db.ForeignKey('department.id', ondelete="CASCADE"),
        nullable=False)
    def __repr__(self):
        return f"employee: {self.name} {self.surname}"


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"department: {self.name}"


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    access_level = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"user: {self.name}, {self.password}, {self.access_level}"