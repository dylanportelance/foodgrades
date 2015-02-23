from flask import Flask
from flask.ext.restful import abort, reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)

# Read in restaurant info

id_field = 1 # id is in 2nd column of restaurant data
restaurants = {} # dict of restaurants ("id" -> dict of restaurant data)

with open('grades.txt') as file:
    fields = file.readline().rstrip('\n').rstrip('\r').split('\t') # strings of restaurant data fields 
    for line in file:
        restaurant = line.rstrip('\n').rstrip('\r').split('\t') # list of restaurant values
        restaurants[restaurant[id_field]] = {}
        for i, field in enumerate(fields):
            restaurants[restaurant[id_field]][field] = restaurant[i]
file.close()

# Read in violations info

id_field = 0 # id is in the 1st column of the violations data

with open('violations.txt') as file:
    fields = file.readline().rstrip('\n').rstrip('\r').split('\t') # strings of violation data fields
    for line in file:
        violation = line.rstrip('\n').rstrip('\r').split('\t') # list of violation values
        restaurant_id = violation[id_field]
        if not "violations" in restaurants[restaurant_id]:
            restaurants[restaurant_id]["violations"] = {}
            violation_id = 1 # starts at 1 for each restaurant
        restaurants[restaurant_id]["violations"][str(violation_id)] = {}
        for i, field in enumerate(fields):
            restaurants[restaurant_id]["violations"][str(violation_id)][field] = violation[i]
        violation_id += 1 
file.close()

class AllRestaurantsAPI(Resource):

    def get(self):
        if not restaurants:
            abort(404, message="No Restaurants")
        return restaurants

class RestaurantsWithNameAPI(Resource):

    def get(self, restaurant_name):
        if not restaurants:
            abort(404, message="No Restaurants")
        return [restaurants[key]["BusinessName"] 
                for key in restaurants
                if restaurant_name.lower() in restaurants[key]["BusinessName"].lower()] 

class RestaurantsWithZipAPI(Resource):

    def get(self, restaurant_zip):
        if not restaurants:
            abort(404, message="No Restaurants")
        return [restaurants[key]["ZIP"]
                for key in restaurants
                if restaurant_zip == restaurants[key]["ZIP"]]

class RestaurantsWithIdAPI(Resource):

    def get(self, restaurant_id):
        if not restaurants:
            abort(404, message="No Restaurants")
        if restaurant_id not in restaurants:
            abort(404, message="Restaurant {} doesn't exist".format(restaurant_id))
        return restaurants[restaurant_id]

class ViolationsAPI(Resource):

    def get(self, restaurant_id):
        if not restaurants:
            abort(404, message="No Restaurants")
        if restaurant_id not in restaurants:
            abort(404, message="Restaurant {} doesn't exist".format(restaurant_id))
        return restaurants[restaurant_id]["violations"]

class ViolationsWithIdAPI(Resource):

    def get(self, restaurant_id, violation_id):
        if not restaurants:
            abort(404, message="No Restaurants")
        if violation_id not in restaurants[restaurant_id]["violations"]:
            abort(404, message="Resturant {}, Violation {} doesn't exist".format(restaurant_id, violation_id))    
        return restaurants[restaurant_id]["violations"][violation_id]

api.add_resource(AllRestaurantsAPI, '/api/v1.0/restaurants')
api.add_resource(RestaurantsWithNameAPI, '/api/v1.0/restaurants/name/<restaurant_name>')
api.add_resource(RestaurantsWithZipAPI, '/api/v1.0/restaurants/zip/<restaurant_zip>')
api.add_resource(RestaurantsWithIdAPI, '/api/v1.0/restaurants/id/<restaurant_id>')
api.add_resource(ViolationsAPI, '/api/v1.0/restaurants/id/<restaurant_id>/violations')
api.add_resource(ViolationsWithIdAPI, '/api/v1.0/restaurants/id/<restaurant_id>/violations/id/<violation_id>')

if __name__ == '__main__':
    app.run()
