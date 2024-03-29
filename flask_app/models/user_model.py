from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE
from flask import flash
from flask_app.utilities import utilities
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.password=data['password']
        self.email=data['email']
        self.updated_at=data['updated_at']
        self.created_at=data['created_at']

    
    @classmethod
    def create(cls,data):
        query="""
        INSERT INTO users (first_name,last_name,password,email)
        VALUES (%(first_name)s,%(last_name)s,%(password)s,%(email)s)
        """

        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query="""
        SELECT * 
        FROM users
        WHERE id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query,data)
        # if len(results) < 1:
        #     return False #inverted check
        # return cls(results[0])
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_by_email(cls,data):
        query="""
        SELECT * 
        FROM users
        WHERE email = %(email)s;
        """

        results = connectToMySQL(DATABASE).query_db(query,data)
        # if len(results) < 1:
        #     return False #inverted check
        # return cls(results[0])
        if results:
            return cls(results[0])
        return False


    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 1:
            flash("First name field required", 'first_name')
            is_valid = False
        elif len(form_data['first_name']) < 2:
            flash("First name must be at least 2 chars", 'first_name')
            is_valid = False
        if len(form_data['last_name']) < 1:
            flash("Last name required", 'last_name')
            is_valid = False
        elif len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 chars", 'last_name')
            is_valid = False
        if len(form_data['email']) < 1:
            flash("Email required", 'email')
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("email invalid", 'email')
            is_valid = False
        else:
            data = {
                'email': form_data['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                flash("email already exists (hope it's you!)", 'email')
                is_valid = False
        if form_data['password'] == "":
                is_valid = False
        elif not utilities.has_number(form_data['password'] or not utilities.has_uppercase(form_data['password'])):
            flash("password must have at least 1 number and 1 uppercase letter", 'password')
            is_valid = False
        if len(form_data['password']) < 1:
            flash("password must be 8 chars", 'password')
            is_valid = False
        elif not form_data['password'] == form_data['conf_pass']:
            flash("passwords must match", 'password')
            is_valid = False
        return is_valid