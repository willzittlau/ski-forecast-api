# libraries
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import json
# root files
from config import ProdConfig, DevConfig
from env import *

# Initialize app
api = Flask(__name__)

# Configuration
api.config.from_object(DevConfig())
#app.config.from_object(ProdConfig())

# Initialize dB
db = SQLAlchemy(api)
from models import *

# Authentication
auth = HTTPBasicAuth()
@auth.get_password
def get_password(username):
    if username == userpass(): #os.environ['API_User']
        return userpass() #os.environ['API_KEY']
    return None

# Error to JSON
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
@api.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
@api.errorhandler(405)
def not_found(error):
    return make_response(jsonify( { 'error': 'Method not allowed' } ), 405)

# Routes
@api.route('/', methods = ['GET'])
@auth.login_required
def index(): # Redirect to proper API URL path
    return redirect(url_for('get_areas'))

# GET all areas
@api.route('/api/v1/areas', methods = ['GET'])
@auth.login_required
def get_areas():
    # Query dB for all rows and save as dict objects
    # Append to list and serve to user as JSON
    get = []
    areas = Areas.query.all()
    for area in areas:
        area_dict = area.__dict__
        del area_dict['_sa_instance_state']
        get.append(area_dict)
    return jsonify( get )

# GET specific area
@api.route('/api/v1/areas/<name>', methods = ['GET'])
@auth.login_required
def get_area(name):
    # Query dB for all rows and save as dict objects
    get = []
    areas = Areas.query.all()
    for area in areas:
        area_dict = area.__dict__
        del area_dict['_sa_instance_state']
        get.append(area_dict)
    # Check to see if name from URL request exists, and if so return info as JSON
    for dictionary in get:
        if str(name) == dictionary["name"]:
            return jsonify( dictionary )
    # Requested URL doesn't exist in dB
    else:
        abort (404)

# Create area
@api.route('/api/v1/areas', methods = ['POST'])
@auth.login_required
def create_area():
    # Check post datatype
    if not request.get_json():
        abort(400)
    else:
        post = request.get_json()
        # Check keys are correct
        if "name" and "area_type" and "avalanche_forecast" and "coordinates" and "model_elevation" in post:
            values = post.values()
            # Check key-value pairs aren't empty
            for val in values:
                if val == '':
                    abort(400)
            # Convert to dB strings
            name = post["name"]
            area_type = post["area_type"]
            avalanche_forecast = post["avalanche_forecast"]
            coordinates = post["coordinates"]
            model_elevation = post["model_elevation"]
            # Make sure name entry doesn't exit already
            if bool(Areas.query.filter_by(name=name).first()) == True:
                abort (400)
            # Add unique completed entry to dB
            else:
                data = Areas(name, coordinates, avalanche_forecast, area_type, model_elevation)
                db.session.add(data)
                db.session.commit()
        else:
            abort(400)
    return jsonify( post ), 201

# PUT (create / modify) specific area
@api.route('/api/v1/areas/<name>', methods = ['PUT'])
@auth.login_required
def update_area(task_id):
    put = request.get_json()
    convert_to_dict(put)
    return jsonify( { 'task': make_public_task(task[0]) } )

# DELETE specific area
@api.route('/api/v1/areas/<name>', methods = ['DELETE'])
@auth.login_required
def delete_area(name):
    if not request.get_json():
        abort(400)
    delete = request.get_json()
    if delete["name"] == str(name):
        if bool(Areas.query.filter_by(name=delete["name"]).first()) == True:
            db.session.delete(Areas.query.filter_by(name=delete["name"]).first())
            db.session.commit()
    else:
        abort (400)
    return jsonify( delete )

# Run app
if __name__ == '__main__':
    api.run()