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

@app.route("/viewercount",methods=['GET'])
def views():
    args = request.args
    content_id = args['content']
    device_id = args['device']
    start_time = args['start']
    end_time = args['end']
    view = True
    res = task.server_requests(device_id, content_id, start_time, end_time, view)
    return jsonify({'start':start_time,'end':end_time,'device':device_id,'content':content_id,'views':res})

@app.route("/create_events", methods=['POST'])
def create_events():
    data = request.get_json()
    new_row=Event(content_ID=data['content_ID'], device_ID=data['device_ID'], start_time=data['start_time'], end_time=data['end_time'])
    db.session.add(new_row)
    db.session.commit()
    return jsonify({'message':'new row created for events'})


@app.route("/get_all_events", methods=['GET'])
def getall_events():
    session = load_session()
    events= session.query(events).all()
    print(events)
    output=[]
    for event in events:
        event_data={}
        event_data['id']=event.id
        event_data['content_ID']=event.content_ID
        event_data['device_ID']=event.device_ID
        event_data['start_time']=event.start_time
        event_data['end_time']=event.end_time
        output.append(event_data)

    return jsonify({'events': output})

if __name__ == '__main__':
    app.run(debug=True)
