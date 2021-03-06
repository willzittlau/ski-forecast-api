# libraries
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import json
import os
# root files
from config import ProdConfig, DevConfig
#from env import *

# Initialize app
api = Flask(__name__)

# Configuration
#api.config.from_object(DevConfig())
api.config.from_object(ProdConfig())

# Initialize dB
db = SQLAlchemy(api)
from models import *

# Authentication
auth = HTTPBasicAuth()
@auth.get_password
def get_password(username):
    if username == os.environ['API_User']: #userpass()
        return os.environ['API_KEY'] #userpass()
    return None

# JSONify error codes
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
    template = {"area_type":"\'backcountry\' or \'resort\'", 
                "avalanche_forecast": "values from https://www.avalanche.ca/api/bulletin-archive/2020/regions.json", 
                "coordinates":"format = \'lat=49.63297&lon=-123.08596\' (from spotWX)", 
                "NAM_elevation":"1149m (NAM elevation from SpotWX)", 
                "HRDPS_elevation":"1249m (HRDPS elevation from SpotWX)",
                "tz_info":"America/Vancouver (tz from SpotWX)",
                "name":"sky-pilot (Area name to be displayed)"
                }
    return jsonify ( template )

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

# POST (create) area
@api.route('/api/v1/areas', methods = ['POST'])
@auth.login_required
def create_area():
    # Check post datatype
    if not request.get_json():
        abort(400)
    else:
        post = request.get_json()
        # Check keys are correct
        if "name" and "area_type" and "avalanche_forecast" and "coordinates" and "tz_info" and "NAM_elevation" and "HRDPS_elevation" in post:
            values = post.values()
            # Check key-value pairs aren't empty
            for val in values:
                if val == '':
                    abort(400)
            # Convert to dB strings
            name = post["name"]
            coordinates = post["coordinates"]
            avalanche_forecast = post["avalanche_forecast"]
            area_type = post["area_type"]
            tz_info = post["tz_info"]
            NAM_elevation = post["NAM_elevation"]
            HRDPS_elevation = post["HRDPS_elevation"]
            # Make sure name entry doesn't exist already
            if bool(Areas.query.filter_by(name=name).first()) == True:
                abort (400)
            # Add unique completed entry to dB
            else:
                data = Areas(name, coordinates, avalanche_forecast, area_type, tz_info, NAM_elevation, HRDPS_elevation)
                db.session.add(data)
                db.session.commit()
        else:
            abort(400)
    return jsonify( post ), 201

# PUT (create / modify) specific area
@api.route('/api/v1/areas/<name>', methods = ['PUT'])
@auth.login_required
def modify_area(name):
    # Check post datatype
    if not request.get_json():
        abort(400)
    else:
        put = request.get_json()
        # Check keys are correct
        if "name" and "area_type" and "avalanche_forecast" and "coordinates" and "tz_info" and "NAM_elevation" and "HRDPS_elevation" in put:
            values = put.values()
            # Check key-value pairs aren't empty
            for val in values:
                if val == '':
                    abort(400)
            # Convert to dB strings
            name = put["name"]
            coordinates = put["coordinates"]
            avalanche_forecast = put["avalanche_forecast"]
            area_type = put["area_type"]
            tz_info = put["tz_info"]
            NAM_elevation = put["NAM_elevation"]
            HRDPS_elevation = put["HRDPS_elevation"]
            # Check if name entry exists
            if bool(Areas.query.filter_by(name=name).first()) == True:
                # Modify selected area
                area = Areas.query.filter_by(name=name).first()
                area.name = name
                area.coordinates = coordinates
                area.avalanche_forecast = avalanche_forecast
                area.area_type = area_type
                area.tz_info = tz_info
                area.NAM_elevation = NAM_elevation
                area.HRDPS_elevation = HRDPS_elevation
                # Submit changes to dB
                db.session.commit()
            # Add entry to dB if it doesn't already exist
            else:
                data = Areas(name, coordinates, avalanche_forecast, area_type, tz_info, NAM_elevation, HRDPS_elevation)
                db.session.add(data)
                db.session.commit()
                return jsonify( put ), 201
        else:
            abort(400)
    return jsonify( put )

# DELETE specific area
@api.route('/api/v1/areas/<name>', methods = ['DELETE'])
@auth.login_required
# Check delete datatype
def delete_area(name):
    if not request.get_json():
        abort(400)
    # Check that contents of delete request match the url route
    delete = request.get_json()
    if delete["name"] == str(name):
        # Check that delete request name exists in dB and execute request
        if bool(Areas.query.filter_by(name=delete["name"]).first()) == True:
            db.session.delete(Areas.query.filter_by(name=delete["name"]).first())
            db.session.commit()
        else:
            abort (404)
    else:
        abort (400)
    return jsonify( delete )

# Run app
if __name__ == '__main__':
    api.run()