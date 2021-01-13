import pymongo
from flask import Flask, jsonify
from database.db import initialize_db
from api.routes.api_routes import api
from api.helpers.errors import APIError
import traceback
import pry
import os
from pymongo import MongoClient


app = Flask(__name__, template_folder = 'api/views')


client = pymongo.MongoClient(os.environ.get('MONGODB_URI'))
db = client.dreamhome

app.register_blueprint(api)
initialize_db(app)

@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {
        "data": {
            "error": err.description,
            "message": ""
        }
    }
    if len(err.args) > 0:
        response["data"]["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors
    app.logger.error(f"{err.description}: {response['data']['message']}")
    return jsonify(response), err.code

@app.errorhandler(500)
def handle_exception(err):
    """Return JSON instead of HTML for any other server error"""
    app.logger.error(f"Unknown Exception: {str(err)}")
    app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
    response = {
        "data": {
            "error": "Sorry, that error is on us, please contact support if this wasn't an accident"
        }
    }
    return jsonify(response), 500

if __name__ == 'main':
    app.run(threaded=True)
