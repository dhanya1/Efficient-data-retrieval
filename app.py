from flask import Flask, request, jsonify
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer
import task

app = Flask(__name__)

class events(object):
    pass

class persons(object):
    pass

def load_session():
    engine = create_engine('sqlite:////users/mscdsa2018/dsj1/advertima/advertima.db', echo=True)
    metadata = MetaData(engine)
    event = Table('event', metadata, Column("event_id", Integer, primary_key=True), autoload=True)
    mapper(events, event)
    #persons = Table('person', metadata, autoload = True)
    #mapper(persons, person)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

'''
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_ID = db.Column(db.String(100))
    device_ID = db.Column(db.String(100))
    start_time = db.Column(db.Text(100))
    end_time = db.Column(db.Text(100))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100))
    appears = db.Column(db.Text(100))
    disappears = db.Column(db.Text(100))
    age = db.Column(db.String(100))
    gender = db.Column(db.String(100))
'''
#db.create_all()
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/viewer-count",methods=['GET'])
def views():
    args = request.args.to_dict()
    args['request'] = 'view'
    args['view'] = task.server_requests(**args)
    return jsonify(args)

@app.route("/avg-age", methods=['GET'])
def avg_age():
    args = request.args.to_dict()
    args['request'] = 'avg_age'
    args['avg_age'] = task.server_requests(**args)
    return jsonify(args)


@app.route("/gender-dist", methods=['GET'])
def getall_events():
    args = request.args.to_dict()
    args['request'] = 'gender_dist'
    args['gender_dist'] = task.server_requests(**args)
    return jsonify(args)


if __name__ == '__main__':
    app.run(debug=True)
