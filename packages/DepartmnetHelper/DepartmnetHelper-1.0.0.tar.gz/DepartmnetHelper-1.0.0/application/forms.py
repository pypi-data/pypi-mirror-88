
from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField ,DateField ,SelectField, validators

from application.models import Department

class AddEmployeeForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=25)])
    surname = StringField('Surname', [validators.Length(min=3, max=25)])
    salary = IntegerField("Salary")
    date_of_birth = DateField("Date Of Birth")
    department = SelectField('Department', coerce=int)
 

class CreateDepartment(Form):
    name = StringField('Name', [validators.Length(min=3, max=25)])


class LogIn(Form):
    name = StringField('Name', [validators.Length(min=3, max=25)])
    password = PasswordField('Password', [validators.Length(min=3, max=25)])
    remember = BooleanField("Remember")


class CreateUser(Form):
    name = StringField('Name', [validators.Length(min=3, max=25)])
    password = PasswordField('Password', [validators.Length(min=3, max=25)])
    password_check = PasswordField('Repeat Password', [validators.Length(min=3, max=25)])
    access_level =  SelectField('Access Level', choices=[(1, 'Standart'), (2, 'Admin')])


class EditUser(Form):
    name = StringField('Name', [validators.Length(min=3, max=25)])
    password = PasswordField('Password', [validators.Length(min=3, max=25)])
    password_check = PasswordField('Repeat Password', [validators.Length(min=3, max=25)])

