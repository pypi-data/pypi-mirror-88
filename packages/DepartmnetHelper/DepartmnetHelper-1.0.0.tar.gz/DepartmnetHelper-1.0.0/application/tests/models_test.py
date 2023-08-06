import pytest

from application import models


def test_employee_model():
    model = models.Employee(
        name="Yura",
        surname="Kulc",
        salary=10000,
        date_of_birth="2016-08-12",
        department_ref=2
    )
    assert str(model) ==  "employee: Yura Kulc"


def test_department_model():
    model = models.Department(
        name="Yura",
    )
    assert str(model) ==  "department: Yura"



def test_user_model():
    model = models.User(
        name="Yura",
        password="Kulc",
        access_level=1,
    )
    assert str(model) == "user: Yura, Kulc, 1"


