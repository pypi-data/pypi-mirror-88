import os

from flask import Flask,request,render_template,redirect, url_for, redirect, flash
from flask_login import login_user, login_required, current_user, logout_user

from application import app
from application.forms import AddEmployeeForm
from application.forms import CreateDepartment
from application.forms import LogIn
from application.forms import CreateUser
from application.forms import EditUser
from application import services

from application import login_manager
 
login_manager.login_view = "login"

@app.route('/', methods=['GET'])
@login_required
def main():
    departments = services.get_department()
    return render_template('show_department.html', departments=departments)


@app.route('/add_department', methods=['POST', 'GET'])
@login_required
def add_department():
    form = CreateDepartment(request.form)
    if request.method == "POST":
        if  form.validate():
            services.create_department(name=form.name.data)
            return redirect(url_for('main'))
        return "error in form"
    return render_template('add_department.html', form=form)


@app.route('/edit_department/<int:dep_id>', methods=['POST', 'GET'])
@login_required
def edit_department(dep_id):
    form = CreateDepartment(request.form)
    if request.method == "POST":
        if  form.validate():
            services.edit_department(id=dep_id,name=form.name.data)
            return redirect(url_for('main'))
        return "error in form"
    return render_template('edit_department.html', form=form)


@app.route("/delete_department/<int:dep_id>", methods=["GET"])
@login_required
def delete_department(dep_id):
    services.delete_department(dep_id)
    return redirect(url_for('main'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LogIn(request.form)
    if request.method == "POST":
        if  form.validate():
            user = services.find_user_by_name(name= form.name.data, password=form.password.data)
            if user is not None:
                login_user(user, remember=form.remember.data)
                return redirect(request.args.get('next')or url_for('main'))
        return "invalid data"
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return services.find_user_by_id(int(user_id)) 


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/add_employee/<int:dep_id>', methods=['POST', 'GET'])
@login_required
def add_employee(dep_id):
    form = AddEmployeeForm(request.form)
    form.department.choices = [*zip([i.id for i in services.get_department()],[i.name for i in services.get_department()])]
    if request.method == "POST" and form.validate():
        services.create_employee( 
            name=form.name.data, 
            surname=form.surname.data,
            salary=form.salary.data, 
            date_of_birth=form.date_of_birth.data, 
            department=form.department.data
        )
        return redirect(url_for('show_employee', dep_id=dep_id))
    return render_template('add_employee.html', form=form)


@app.route('/show_employee/<int:dep_id>', methods=['GET'])
@login_required
def show_employee(dep_id):
    employees =  services.find_employees_by_dep_ref(int(dep_id))
    return render_template('show_employee.html', employees=employees, dep_id=dep_id)


@app.route("/edit_employee/<int:dep_id>/<int:id>", methods=["GET", "POST"])
@login_required
def edit_employee(dep_id,id):
    employee = services.find_employee_by_id(id)
    form = AddEmployeeForm(request.form)
    form.department.choices = [*zip([i.id for i in services.get_department()],[i.name for i in services.get_department()])]
    if request.method == "POST" and form.validate():
        services.update_employee(
            id=id,
            name=form.name.data,
            surname=form.surname.data,
            salary=form.salary.data,
            date_of_birth=form.date_of_birth.data,
            department=form.department.data
        )
        return redirect(url_for('show_employee',dep_id=dep_id))
    return render_template('edit_employee.html',form=form, employee=employee)


@app.route("/delete_employee/<int:dep_id>/<int:id>", methods=["GET"])
@login_required
def delete_employee(dep_id,id):
    services.delete_employee(id)
    return redirect(url_for('show_employee', dep_id=dep_id))


@app.route("/add_user", methods=['POST', 'GET'])
@login_required
def add_user():
    form = CreateUser(request.form)
    if request.method == "POST" and form.validate():
        user_with_the_same_name = services.get_user_by_name(form.name.data)
        if form.password.data == form.password_check.data and not user_with_the_same_name:
            services.create_user(
                name=form.name.data,
                password=form.password.data,
                access_level=form.access_level.data
            )
            return redirect(url_for('main'))
    return render_template('add_user.html',form=form)


@app.route("/edit_user", methods=['POST', 'GET'])
@login_required
def edit_user():
    form = EditUser(request.form)
    print(request.form)
    if request.method == "POST" and form.validate():
        if form.password.data == form.password_check.data:
            services.update_user(
                id=current_user.id,
                name=form.name.data,
                password=form.password.data
            )
           
        return redirect(url_for('main'))
    return render_template('edit_user.html',form=form)


