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
    kwargs['content_start'] = min(content_output['start_time'])
    kwargs['content_end'] = max(content_output['end_time'])

    sql = "select * from person \
    where device_ID = {device_id} and  \
    max(appears,'{start_time}') <  min(disappears, '{end_time}') and \
    appears < '{content_end}' and disappears > '{content_start}'".format(**kwargs)
    cur.execute(sql)
    person_output = pd.read_sql(sql,conn).reset_index(drop=True)
    type(person_output['appears'][0])
    person_output['appears'] = pd.to_datetime(person_output['appears'],format='%Y-%m-%d %H:%M:%S')
    person_output['disappears'] = pd.to_datetime(person_output['disappears'],format='%Y-%m-%d %H:%M:%S')
    if len(person_output.index) == 0:
        return exception(kwargs['request'])
    count = 0; age = 0; male =0; female =0;
    b = list(range(len(content_output.index)))
    new_data = pd.DataFrame() 
    for j in b:
        rows = (person_output['appears']<=content_output['end_time'][j]) & (person_output['disappears'] >= content_output['start_time'][j])
        #rows = max(person_output['appears'],content_output['start_time'][j]) < min(content_output['end_time'][j], person_output['disappears']) 
        rows1 = (person_output['appears']<= person_output['disappears']) & (content_output['start_time'][j]<=content_output['end_time'][j]) 
        new_data = pd.concat([new_data,person_output.loc[rows1&rows]])
    count = len(new_data.index)
    if kwargs['request'] == 'avg_age':
        return sum(new_data['age'])/count
    elif kwargs['request'] == 'gender_dist':
        male = len(new_data.loc[(new_data['gender'] == 'male')].index)
        female = len(new_output.loc[(new_data['gender'] == 'female')].index)
        return {'male':male/count,'female':female/count}
    else:
        return count

a = {'device_id' :5, 'content_id':2, 'start_time':"2016-01-31 00:00:00", 'end_time':"2016-01-31 00:01:41",'request':'count'}
t0 = time.time()
print(server_requests(**a))
t1 = time.time()
print(t1-t0)
