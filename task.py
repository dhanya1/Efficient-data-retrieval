from database import database
import pandas as pd

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
    
