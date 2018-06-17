from flask import Flask, request, jsonify
from datetime import datetime
import task
import sys

app = Flask(__name__)


def validate_request(**args):
    '''
    Validate the url requested is valid
    :param args:
    :return: Error if any
    '''
    error = ''
    try:
        int(args['device_id'])
        int(args['content_id'])
    except ValueError:
        error = 'BadURL: Device and Content ID must be an integer'
    except KeyError:
        error = 'BadURL:Device and Content ID must be specified'
    except:
        error = 'Unexpected error: {}'.format(sys.exc_info()[0])

    try:
        datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S')
        datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        error = 'BadURL: Date should be in format YYYY-MM-DD HH:MM:SS'
    except KeyError:
        error = 'BadURL: Start and End date time duration must be specified'
    return error


def function(**args):
    '''
    Validate the url requested is valid
    :param args:
    :return: Error if any
    '''
    error = validate_request(**args)
    result = ''
    if error == '':
        try:
            result = task.server_requests(**args)
            print(result)
        except:
            error = "Unexpected error: {}".format(sys.exc_info()[0])
    return result,error


@app.route("/")
def hello():
    return "Advertima API Home Page"


@app.route("/viewer-count",methods=['GET'])
def views():
    args = request.args.to_dict()
    args['request'] = 'view'
    (result,error) = function(**args)
    print(error)
    if error != '':
        args['error'] = error
    else:
        args['view'] = result
    return jsonify(args)


@app.route("/avg-age", methods=['GET'])
def avg_age():
    args = request.args.to_dict()
    args['request'] = 'avg_age'
    (result,error) = function(**args)
    if error != '':
        args['error'] = error
    else:
        args['avg_age'] = result
    return jsonify(args) 


@app.route("/gender-dist", methods=['GET'])
def getall_events():
    args = request.args.to_dict()
    args['request'] = 'gender_dist'
    (result,error) = function(**args)
    if error != '':
        args['error'] = error
    else:
        args['gender_dist'] = result
    return jsonify(args)


if __name__ == '__main__':
    app.run(debug=True)
