from application import db
from application.models import Department
from application.models import User
from application.models import Employee

def get_department():
    return Department.query.all()

def create_department(name):
    department = Department(name=name)
    db.session.add(department)
    db.session.commit()

def edit_department(id, name):
    Department.query.filter_by(id=id).update(dict(name=name))
    db.session.commit()


def delete_department(dep_id):
    Department.query.filter_by(id=dep_id).delete()
    db.session.commit()


def find_user_by_name(name, password):
    return User.query.filter_by(name=name, password=password).first()


def find_user_by_id(user_id):
    return User.query.get(int(user_id))


def create_employee(name, surname, salary, date_of_birth, department):
        employee = Employee(
            name=name, 
            surname=surname,
            salary=salary, 
            date_of_birth=date_of_birth, 
            department_ref=department
        )
        db.session.add(employee)
        db.session.commit()


def find_employees_by_dep_ref(dep_id):
    return Employee.query.filter_by(department_ref=int(dep_id))


def find_employee_by_id(id):
    return Employee.query.get(int(id))


def update_employee(id, name, surname, salary, date_of_birth, department):
        Employee.query.filter_by(id=id).update(dict(
            name=name,
            surname=surname,
            salary=salary,
            date_of_birth=date_of_birth,
            department_ref=department
            )
        )
        db.session.commit()


def delete_employee(id):
    Employee.query.filter_by(id=id).delete()
    db.session.commit()


def create_user(name, password, access_level):
    user = User(
            name=name,
            password=password,
            access_level=access_level
            )
    db.session.add(user)
    db.session.commit()


def update_user(id, name, password):
    User.query.filter_by(id=id).update(dict(name=name, password=password))
    db.session.commit()

def get_user_by_name(name):
    return User.query.filter_by(name=name).all()


