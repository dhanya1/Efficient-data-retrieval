from flask import Flask, request, jsonify
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer
import task
import datetime

app = Flask(__name__)

def validate_request(**args):
    try:
        a = int(args['device_id'])
        b = int(args['content_id'])
    except:
        error = 'BadURL: Device and Content ID must be an integer'
    return error

def function(**args):
    args = request.args.to_dict()
    error = validate_request(args)
    if not error:
        try:
            result = task.server_requests(**args)
        except:
            error = 'Error occured'
    return result,error

@app.route("/")
def hello():
    return "Advertima API Home Page"

@app.route("/viewer-count",methods=['GET'])
def views():
    args = request.args.to_dict()
    args['request'] = 'view'
    (result,error) = function(args)
    if error: 
        args['error'] = error
    else:
        args['view'] = result
    return jsonify(args)

@app.route("/avg-age", methods=['GET'])
def avg_age():
    args = request.args.to_dict()
    args['request'] = 'avg_age'
    (result,error) = function(args)
    if error: 
        args['error'] = error
    else:
        args['avg_age'] = result
    return jsonify(args) 


@app.route("/gender-dist", methods=['GET'])
def getall_events():
    args = request.args.to_dict()
    args['request'] = 'gender_dist'
    (result,error) = function(args)
    if error:   
        args['error'] = error
    else:
        args['gender_dist'] = result
    return jsonify(args)

if __name__ == '__main__':
    app.run(debug=True)
