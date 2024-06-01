from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
user = os.environ["DB_USER"]
password = os.environ["DB_PASSWORD"]
host = os.environ["DB_HOST"]
dbname = os.environ["DB_NAME"]
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{dbname}'
db_obj = SQLAlchemy(app)


class Employee(db_obj.Model):
    __tablename__ = "employee"
    empid = db_obj.Column(db_obj.Integer,primary_key=True)
    name = db_obj.Column(db_obj.Text)
    email = db_obj.Column(db_obj.Text)
    salary = db_obj.Column(db_obj.Integer)
    department = db_obj.Column(db_obj.Text)
