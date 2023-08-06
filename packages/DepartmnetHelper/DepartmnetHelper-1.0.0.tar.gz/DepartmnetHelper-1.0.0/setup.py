from setuptools import find_packages, setup

setup(
    name='DepartmnetHelper',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author='YuraKulchytskiy',
    url="",
    author_email="kulchytskiyyura@gmail.com",
    install_requires=[
        'pytest',
        'flask',
        'wtforms',
        'flask_sqlalchemy',
        'flask_migrate'

    ],
)