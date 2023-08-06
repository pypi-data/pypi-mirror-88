import pytest
import sys
from flask import template_rendered
from contextlib import contextmanager
import json
from unittest.mock import MagicMock
from flask_login import UserMixin

from application import views



class SessionMock:
    def add(*args, **kwargs):
        pass

    def commit(*args, **kwargs):
        pass


class DbMock:
    session = SessionMock()


@pytest.fixture
def captured_templates(test_app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record,  test_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, test_app)


def test_main_with_render(client, login_for_test, captured_templates, monkeypatch):
    monkeypatch.setattr('application.views.services.get_department', lambda *args,**kwargs:[])
    response = client.get("/",)
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "show_department.html"
    assert "departments" in context
   

def test_main_without_render(client, login_for_test, monkeypatch):
    def all(*args, **kwargs):
        return ["department1", "department2"]
    
    def mock_render_template(template, **kwargs):
        return json.dumps({"template":template,**kwargs})

    monkeypatch.setattr('application.views.services.get_department', all)
    monkeypatch.setattr('application.views.render_template', mock_render_template)
    response = client.get("/")
    data = json.loads(response.data)
    assert data["template"] == "show_department.html"
    assert data["departments"] == ["department1", "department2"]


def test_add_department_get(client, login_for_test, captured_templates):
    response = client.get("/add_department")
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "add_department.html"
    assert "form" in context
    assert context["form"].name.data == ""


def test_add_department_post(client, login_for_test, monkeypatch, captured_templates):
    monkeypatch.setattr('application.views.services.create_department',lambda *args,**kwargs:0)
    response = client.post("/add_department", data=dict(name="Yura"))
    assert response.status_code == 302


@pytest.mark.parametrize(
    "name", 
    [
        "ma",
        "ljljljljlljljljljlljljljlljljlljljljljljljlljljljlljlj",
        25
    ]
)
def test_add_department_post_wrong_data(client, login_for_test, monkeypatch, captured_templates,name):
    response = client.post("/add_department", data=dict(name=name))
    monkeypatch.setattr('application.views.services.create_department',lambda *args,**kwargs:0)
    assert response.status_code == 200
    assert response.data == b"error in form"


def test_login_get(client, login_for_test, captured_templates):
    response = client.get("/login")
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "login.html"
    assert "form" in context
    assert context["form"].name.data == ""
    assert context["form"].password.data == ""
    assert context["form"].remember.data == False


@pytest.mark.parametrize(
    "name, password, remember", 
    [
        ("Yura","1111",True),
        ("Yura","1111",False),
        ("Yura_1","andrii",True)
    ]
)
def test_login_post(client, login_for_test, monkeypatch, name, password, remember):
    def find_user_by_name_mock(*args,**kwargs):
            return "value"
    
    monkeypatch.setattr('application.views.services.find_user_by_name',find_user_by_name_mock)
    monkeypatch.setattr('application.views.login_user', lambda *args, **kwargs:0)
    response = client.post("/login", data=dict(name=name,password=password,remember=remember))
  
    assert response.status_code == 302


@pytest.mark.parametrize(
    "name, password, remember, return_value", 
    [
        ("Ya","1111",True,"value"),
        ("Yura","11",False,"value"),
        ("Yura_1","andrii",True, None),

        ("tooooooo_looooooong_striiiiiiiiiiiing___________","andrii",True, "value"),
        ("Yura","tooooooo_looooooong_striiiiiiiiiiiing__________",True, "value")

    ]
)
def test_login_post(client, login_for_test, monkeypatch, name, password, remember, return_value):
    def find_user_by_name_mock(*args,**kwargs):
            return return_value
    
    monkeypatch.setattr('application.views.services.find_user_by_name',find_user_by_name_mock)
    monkeypatch.setattr('application.views.login_user', lambda *args, **kwargs:0)
    response = client.post("/login", data=dict(name=name,password=password,remember=remember))
  
    assert response.status_code == 200
    assert response.data == b"invalid data"



@pytest.mark.parametrize(
    "dep_id", 
    [
        7,
        5,
        120

    ]
)
def test_delete_department(client, login_for_test, monkeypatch, dep_id):
    def delete_mock(id,*args,**kwargs):
            if id != dep_id:
                raise Exception("id in filter_by is diiferent then input department id")
            return None

    monkeypatch.setattr('application.views.services.delete_department',  delete_mock)
    response = client.get(f"/delete_department/{dep_id}")
    assert response.status_code == 302


@pytest.mark.parametrize(
    "dep_id", 
    [
        "45",
        "457"   
    ]
)
def test_delete_department_error_raise(client, login_for_test, monkeypatch, dep_id):
    def delete_mock(id, *args,**kwargs):
            if id != dep_id:
                raise Exception("id in filter_by is diiferent then input department id")
            return None

    monkeypatch.setattr('application.views.services.delete_department',  delete_mock)
    with pytest.raises(Exception):
        response = client.get(f"/delete_department/{dep_id}")
        assert response.status_code == 200


@pytest.mark.parametrize(
    "dep_id", 
    [
        "45.256",
        "wrong data"   
    ]
)
def test_delete_department_wrong_data(client, login_for_test, monkeypatch, dep_id):
    def delete_mock(id, *args,**kwargs):
            if id != dep_id:
                raise Exception("id in filter_by is diiferent then input department id")
            return None

    monkeypatch.setattr('application.views.services.delete_department',  delete_mock)
   
    response = client.get(f"/delete_department/{dep_id}")
    assert response.status_code == 404


def test_logout(client, login_for_test, monkeypatch):
    monkeypatch.setattr('application.views.logout_user', lambda *args, **kwargs:0)
    response = client.get("/logout")
    assert response.status_code == 302
   

def test_add_employee(client, login_for_test, captured_templates, monkeypatch):
    def get_department_mock(*args,**kwargs):
        return []

    monkeypatch.setattr('application.views.services.get_department',  get_department_mock)
    monkeypatch.setattr('application.views.services.create_employee',  lambda *args, **kwargs:0)
    response = client.get("/add_employee/25")
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "add_employee.html"
    assert "form" in context
    assert context["form"].name.data == ""
    assert context["form"].surname.data == ""
    assert context["form"].date_of_birth.data == None
    assert context["form"].salary.data == None
    assert context["form"].department.data == None


@pytest.mark.parametrize(
    "name,surname,date_of_birth,salary,department", 
    [
        ("yura","kulchytskiy","2001-09-20","2140","4"),
        ("Yura","Kulchytskiy","2001-12-10","20","4")   
    ]
)
def test_add_employee_post(client, login_for_test, captured_templates, monkeypatch,\
                            name,surname,date_of_birth,salary,department):
    class UserMock:
        id = 4
        name = "name"
        
    def get_department_mock(*args,**kwargs):
        return [UserMock()]

    monkeypatch.setattr('application.views.services.get_department',  get_department_mock)
    monkeypatch.setattr('application.views.services.create_employee',  lambda *args, **kwargs:0)
    response = client.post("/add_employee/25",data=dict(
        name=name,
        surname=surname,
        date_of_birth=date_of_birth,
        salary=salary,
        department=department
        ),
        follow_redirects=True)
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "show_employee.html"
    assert "dep_id" in context
    assert context["dep_id"] == 25  


@pytest.mark.parametrize(
    "name,surname,date_of_birth,salary,department", 
    [
        ("yus","kulchytskiy","2001.09.12","2140","4"),
        ("Yura","Kulchytskiy","2001-12-10","20","5"),
        ("Yura","Kulchytskiy","2001-12-78","20","4"),
        ("Yura","Kulchytskiy","2001-12-78","20.45","4"),
        ("Yura","Kulchytskiy","2001-12-78","mama","4"),
        ("Y","Kulchytskiy","2001-12-78","20","4"),
        ("Yura","Ku","2001-12-78","20","4")   
    ]
)
def test_add_employee_wrong_data(client, login_for_test, captured_templates, monkeypatch,\
                            name,surname,date_of_birth,salary,department):
    class UserMock:
        id = 4
        name = "name"
        
    def get_department_mock(*args,**kwargs):
        return [UserMock()]

    monkeypatch.setattr('application.views.services.get_department',  get_department_mock)
    monkeypatch.setattr('application.views.services.create_employee',  lambda *args, **kwargs:0)
    response = client.post("/add_employee/25",data=dict(
        name=name,
        surname=surname,
        date_of_birth=date_of_birth,
        salary=salary,
        department=department
        ),
        follow_redirects=True)
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "add_employee.html"
    assert "form" in context


def test_show_employee(client, login_for_test, captured_templates, monkeypatch):
    class EmployeeMock:
        id = 1
        name = "Yura"
        surname = "kulch"
        salary =  200
        date_of_birth = "2001-12-10"
        department_ref = 2
    
    def find_employees_by_dep_ref_mock(*args,**kwargs):
           return [EmployeeMock()]

    monkeypatch.setattr('application.views.services.find_employees_by_dep_ref', find_employees_by_dep_ref_mock)
    response = client.get("/show_employee/25")
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "show_employee.html"
    assert context["dep_id"] == 25
    assert  context["employees"][0].id == 1
    assert  context["employees"][0].name == "Yura"
    assert  context["employees"][0].surname == "kulch"
    assert  context["employees"][0].salary == 200
    assert  context["employees"][0].date_of_birth ==  "2001-12-10"
    assert  context["employees"][0].department_ref ==  2 


def test_edit_employee_get(client, login_for_test, captured_templates, monkeypatch):
    class EmployeeMock:
        id = 1
        name = "Yura"
        surname = "kulch"
        salary =  200
        date_of_birth = "2001-12-10"
        department_ref = 2
 
    def find_employee_by_id_mock(*args,**kwargs):
            return EmployeeMock()

    class UserMock:
        id = 4
        name = "name"
       
    def get_department_mock(*args,**kwargs):
            return [UserMock()]

    monkeypatch.setattr('application.views.services.find_employee_by_id',  find_employee_by_id_mock)
    monkeypatch.setattr('application.views.services.update_employee', lambda *args,**kwargs:0)
    monkeypatch.setattr('application.views.services.get_department', get_department_mock)
    response = client.get("/edit_employee/25/22")
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "edit_employee.html"
    assert "form" in context
    assert "employee" in context
    assert  context["employee"].id == 1
    assert  context["employee"].name == "Yura"
    assert  context["employee"].surname == "kulch"
    assert  context["employee"].salary == 200
    assert  context["employee"].date_of_birth == "2001-12-10"
    assert  context["employee"].department_ref ==  2 


def test_edit_employee_post(client, login_for_test, captured_templates, monkeypatch):
    class EmployeeMock:
        id = 1
        name = "Yura"
        surname = "kulch"
        salary =  200
        date_of_birth = "2001-12-10"
        department_ref = 4

        def update(*args,**kwargs):
            pass
        def __iter__(self,*args,**kwargs):
            return iter([])

    def find_employee_by_id_mock(*args,**kwargs):
            return EmployeeMock()

    class UserMock:
        id = 4
        name = "name"
       
    def get_department_mock(*args,**kwargs):
            return [UserMock()]


    monkeypatch.setattr('application.views.services.find_employee_by_id',  find_employee_by_id_mock)
    monkeypatch.setattr('application.views.services.update_employee', lambda *args,**kwargs:0)
    monkeypatch.setattr('application.views.services.get_department', get_department_mock)
    response = client.post("/edit_employee/25/22", data=dict(
            name="yura",
            surname="kulchytskiy",
            salary="2140",
            date_of_birth="2001-09-20",
            department="4"
            ),follow_redirects=True)
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "show_employee.html"
    
    assert "dep_id" in context
    assert  context["dep_id"] == 25    


@pytest.mark.parametrize(
    "name,surname,date_of_birth,salary,department", 
    [
        ("yus","kulchytskiy","2001.09.12","2140","4"),
        ("Yura","Kulchytskiy","2001-12-10","20","5"),
        ("Yura","Kulchytskiy","2001-12-78","20","4"),
        ("Yura","Kulchytskiy","2001-12-78","20.45","4"),
        ("Yura","Kulchytskiy","2001-12-78","mama","4"),
        ("Y","Kulchytskiy","2001-12-78","20","4"),
        ("Yura","Ku","2001-12-78","20","4")   
    ]
)
def test_edit_employee_wrong_data(client, login_for_test, captured_templates, monkeypatch,\
                                   name,surname,date_of_birth,salary,department):
    class EmployeeMock:
        id = 1
        name = "Yura"
        surname = "kulch"
        salary =  200
        date_of_birth = "2001-12-10"
        department_ref = 4

        def update(*args,**kwargs):
            pass
        def __iter__(self,*args,**kwargs):
            return iter([])

    def find_employee_by_id_mock(*args,**kwargs):
            return EmployeeMock()

    class UserMock:
        id = 4
        name = "name"
       
    def get_department_mock(*args,**kwargs):
            return [UserMock()]


    monkeypatch.setattr('application.views.services.find_employee_by_id',  find_employee_by_id_mock)
    monkeypatch.setattr('application.views.services.update_employee', lambda *args,**kwargs:0)
    monkeypatch.setattr('application.views.services.get_department', get_department_mock)
    response = client.post("/edit_employee/25/22", data=dict(
             name=name,
             surname=surname,
             date_of_birth=date_of_birth,
             salary=salary,
             department=department
            ),follow_redirects=True)
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "edit_employee.html"
    
    assert "form" in context
    assert "employee" in context


def test_delete_employee(client, login_for_test, captured_templates, monkeypatch):
    
    monkeypatch.setattr('application.views.services.delete_employee', lambda *args, **kwargs:0)
    
    response = client.get("/delete_employee/11/22",follow_redirects=True)

    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "show_employee.html"
    
    assert "dep_id" in context
    assert  context["dep_id"] == 11


def test_add_user_get(client, login_for_test, captured_templates):
    response = client.get("/add_user")
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "add_user.html"
    assert "form" in context


def test_add_user_post(client, login_for_test, captured_templates, monkeypatch):
    monkeypatch.setattr('application.views.services.get_user_by_name', lambda *args,**kwargs:False)
    monkeypatch.setattr('application.views.services.create_user', lambda *args,**kwargs:0)
  
    response = client.post("/add_user", data=dict(
            name="Uira",
            password="1111",
            password_check="1111",
            access_level="1"
        ),follow_redirects=True)
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "show_department.html"


@pytest.mark.parametrize(
    "return_value,name,password,password_check,access_level", 
    [
        (True,"name","111111","1111",2) ,
        (False,"na","1111","1111",2),
        (True,"name","11","11",2),
        (True,"name","111111","1111",2.3)
    ]
)
def test_add_user_post_wrong_data(client, login_for_test, captured_templates, monkeypatch,
                        return_value,name,password,password_check,access_level):

    monkeypatch.setattr('application.views.services.get_user_by_name', lambda *args,**kwargs:return_value)
    monkeypatch.setattr('application.views.services.create_user', lambda *args,**kwargs:0)
    response = client.post("/add_user", data=dict(
            name=name,
            password=password,
            password_check=password_check,
            access_level=access_level
        ),follow_redirects=True)
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "add_user.html"


def test_edit_user(client, login_for_test, captured_templates):
    response = client.get("/edit_user")
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "edit_user.html"
    assert "form" in context
