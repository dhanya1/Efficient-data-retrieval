import pandas as pd
import sqlite3
import time

def exception(request_name):
    if request_name == 'view':
        return 0
    elif request_name == 'avg_age':
        return 0
    elif request_name == 'gender_dist':
        return {'male':0,'female':0}



def server_requests(**kwargs):
    conn = sqlite3.connect("advertima.db")
    cur = conn.cursor()
    sql = "select start_time,end_time from event\
    where device_id = {device_id} and content_id={content_id} \
    and max(start_time, '{start_time}') < min(end_time, '{end_time}')".format(**kwargs)
    content_output = pd.read_sql(sql,conn).reset_index(drop=True)
    if len(content_output.index) == 0:
        return exception(kwargs['request'])
    content_output['start_time'] = pd.to_datetime(content_output['start_time'],format='%Y-%m-%d %H:%M:%S')
    content_output['end_time'] = pd.to_datetime(content_output['end_time'],format='%Y-%m-%d %H:%M:%S')


    sql = "select * from person \
    where device_ID = {device_id} and  \
    max(appears,'{start_time}') <  min(disappears, '{end_time}')".format(**kwargs)
    cur.execute(sql)
    person_output = pd.read_sql(sql,conn).reset_index(drop=True)
    type(person_output['appears'][0])
    person_output['appears'] = pd.to_datetime(person_output['appears'],format='%Y-%m-%d %H:%M:%S')
    person_output['disappears'] = pd.to_datetime(person_output['disappears'],format='%Y-%m-%d %H:%M:%S')
    if len(person_output.index) == 0:
        return exception(kwargs['request'])
    count = 0; age = 0; male =0; female =0;
    a = list(range(len(person_output.index)))
    b = list(range(len(content_output.index)))
    for j in b:
        for i in a:
            if max(person_output['appears'][i],content_output['start_time'][j]) <= \
            min(person_output['disappears'][i],content_output['end_time'][j]):
                count+=1
                if kwargs['request'] == 'avg_age':
                    age += person_output['age'][i]
                if kwargs['request'] == 'gender_dist':
                    if person_output['gender'][i] == 'male':
                        male +=1
                    elif person_output['gender'][i] == 'female':
                        female +=1
                    else:
                        pass

    if kwargs['request'] == 'avg_age':
        return age/count
    elif kwargs['request'] == 'gender_dist':
        return {'male':male/count,'female':female/count}
    else:
        return count

a = {'device_id' :5, 'content_id':2, 'start_time':"2016-01-31 00:00:00", 'end_time':"2016-01-31 00:01:41",'request':'avg_age'}
print(server_requests(**a))
