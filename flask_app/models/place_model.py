from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE
from flask import flash
from flask_app.utilities import utilities

class Place:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.description = data['description']
        self.lat = data['lat']
        self.lng = data['lng']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'lat': self.lat,
            'lng': self.lng,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_id': self.user_id
        }
    
    #remove the created at and updated at for json conversion
    def remove_date(self):
        """
        :params: self
        :returns: none
        """
        del self.created_at
        del self.updated_at


#add a place
    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO places (name,type,description,lat,lng,user_id)
        VALUES (%(name)s,%(type)s,%(description)s,%(lat)s,%(lng)s,%(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)


#update a place
    @classmethod
    def update(cls,data):
        query="""
        UPDATE places
        SET name = %(name)s, type = %(type)s, description = %(description)s, lat= %(lat)s, lng= %(lng)s
        WHERE id = %(id)s
        """
        return connectToMySQL(DATABASE).query_db(query,data)


#delete a place
    @classmethod
    def delete(cls,data):
        query="""
        DELETE FROM places
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


#the method to get all places
    @classmethod
    def get_all(cls):
        query="""
        SELECT * 
        FROM places;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            places_list = []
            for one_row in results:
                one_place = cls(one_row).to_dict()
                places_list.append(one_place)
            return places_list
        return False

    @classmethod
    def get_one(cls,data):

        query = """
        SELECT *
        FROM places
        WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results[0])
        return cls(results[0])


    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 1:
            is_valid = False
            flash("Please enter the name", "name")
        if len(form_data['description']) < 1:
            is_valid = False
            flash("You must provide a description", "description")
        if len(form_data['type'])<1:
            is_valid = False
            flash("please specify the type of location", "type")
        
        #update the location with the google api
        # if len(form_data['location']) < 1:
        #     is_valid = False
        # flash("Please specify a location", "location")
        return is_valid