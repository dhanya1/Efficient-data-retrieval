import pandas as pd
import sqlite3
import time


def server_requests(device_id, content_id, start_time, end_time, view=False, avg_age=False, gender_dist=False):
    conn = sqlite3.connect("advertima.db")
    cur = conn.cursor()
    #args = {'device_id' :1, 'content_id':1, 'start_time':'2016-01-01 00:47:25', 'end_time':'2016-01-01 01:47:25'}
    args = {'device_id' :int(device_id), 'content_id':int(content_id), 'start_time':start_time, 'end_time':end_time}
    sql = "select start_time,end_time from event\
    where device_id = {device_id} and content_id={content_id} \
    and max(start_time, '{start_time}') < min(end_time, '{end_time}')".format(**args)
    content_output = pd.read_sql(sql,conn).reset_index(drop=True)
    content_output['start_time'] = pd.to_datetime(content_output['start_time'],format='%Y-%m-%d %H:%M:%S')
    content_output['end_time'] = pd.to_datetime(content_output['end_time'],format='%Y-%m-%d %H:%M:%S')
    args['end_time'] = str(max(content_output['end_time']))


    sql = "select * from person where device_ID = {device_id} and appears between\
    '{start_time}' and '{end_time}';".format(**args)
    cur.execute(sql)
    person_output = pd.read_sql(sql,conn).reset_index(drop=True)
    type(person_output['appears'][0])
    person_output['appears'] = pd.to_datetime(person_output['appears'],format='%Y-%m-%d %H:%M:%S')
    person_output['disappears'] = pd.to_datetime(person_output['disappears'],format='%Y-%m-%d %H:%M:%S')
    len(person_output.index)


    t0 = time.time()
    count = 0; age = 0; male =0; female =0;
    a = list(range(len(person_output.index)))
    b = list(range(len(content_output.index)))
    for j in b:
        for i in a:
            if max(person_output['appears'][i],content_output['start_time'][j]) <= \
            min(person_output['disappears'][i],content_output['end_time'][j]):
                count+=1
                if avg_age:
                    age += person_output['age'][i]
                if gender_dist:
                    if person_output['gender'][i] == 'male':
                        male +=1
                    elif person_output['gender'][i] == 'female':
                        female +=1
                    else:
                        pass
    t1 = time.time()
    if avg_age:
        return age/count
    elif gender_dist:
        return male/count,female/count
    else:
        return count

#server_requests(1, 1, '2016-01-01 00:47:25', '2016-01-01 01:47:25', view=True)
"""
def get_info_content(device_id, content_id, start_time, end_time):
    '''
    This module retrives information about content displayed on device
    input params:device_id, content_id, start_time, end_time
    '''  
    args = {'device_id':device_id, 'content_id':content_id, 'start_time':start_time,'end_time':end_time}
    sql ='select event_type, event_time from events where device_ID = {device_id} and \
          content_ID = {content_id} and event_time between "{start_time}" and "{end_time}" order by\
          datetime(event_time);'.format(**args)
    db = database()
    conn = db.connect()
    df = pd.DataFrame(db.execute_query(conn,sql),columns = ['event_type','event_time'])
    #df.sort_values(by='event_time')
    print(df)
    df['event_time'] = pd.to_datetime(df["event_time"])
    

def get_info_person(device_id, start_time, end_time):
    '''
    This module returns information about people in front of the device
    during the given time
    input params: device_id, start_time, end_time
    '''
    args = {'device_id':device_id,'start_time':start_time,'end_time':end_time}
    sql ='select * from persons where device_ID = {device_id} and appears between "{start_time}"\
    and "{end_time}" order by datetime(appears);'.format(**args)
    db = database()
    conn = db.connect()
    df = pd.DataFrame(db.execute_query(conn,sql),columns = ['device_ID','appears','disappears','age','gender'])
    print(df)

if __name__=="__main__":
    #get_info_content(2,7,'2016-01-14 14:40:41','2017-01-14 14:40:41')
    get_info_person(2,'2016-01-14 14:40:41','2017-01-14 14:40:41')
"""
