import pandas as pd
import sqlite3


def exception(request_name):
    '''
    Exception handling cases
    '''
    if request_name == 'view':
        return 0
    elif request_name == 'avg_age':
        return 0
    elif request_name == 'gender_dist':
        return {'male':0,'female':0}


def server_requests(**kwargs):
    '''
    Serves the APIs
    '''

    # Database connection
    conn = sqlite3.connect("advertima.db")
    cur = conn.cursor()

    # Retrive the contents whose start or end time overlap with the requested duration
    # for specific device and content id.
    sql = "select start_time,end_time from event\
    where device_id = {device_id} and content_id={content_id} \
    and max(start_time, '{start_time}') < min(end_time, '{end_time}')".format(**kwargs)
    content_output = pd.read_sql(sql,conn).reset_index(drop=True)
    if len(content_output.index) == 0:
        return exception(kwargs['request'])
    content_output['start_time'] = pd.to_datetime(content_output['start_time'],format='%Y-%m-%d %H:%M:%S')
    content_output['end_time'] = pd.to_datetime(content_output['end_time'],format='%Y-%m-%d %H:%M:%S')

    # Store the minimum start time and maximum end time of the content.
    kwargs['content_start'] = min(content_output['start_time'])
    kwargs['content_end'] = max(content_output['end_time'])

    # Retrieve views that overlap the requested period ,
    # while ignoring all people who disappear before minimum content start time
    # or appeared after maximum content end time.
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

    # Calculate the number of times content was played during the duration.
    l = len(content_output.index)
    new_data = pd.DataFrame()

    # Find the rows in persons where times appears and disappears overlap with content_begin and content_end.
    # Concatenate the filtered rows to new_data.
    for j in range(l):
        rows = (person_output['appears']<=content_output['end_time'][j]) & \
               (person_output['disappears'] >= content_output['start_time'][j])
        rows1 = (person_output['appears']<= person_output['disappears']) & \
                (content_output['start_time'][j]<=content_output['end_time'][j])
        new_data = pd.concat([new_data,person_output.loc[rows1&rows]])

    # Gives the number of views.
    count = len(new_data.index)

    # Returns the average age.
    if kwargs['request'] == 'avg_age':
        return round(sum(new_data['age'])/count,1)

    # Returns the gender distribution.
    elif kwargs['request'] == 'gender_dist':
        male = len(new_data.loc[(new_data['gender'] == 'male')].index)
        female = len(new_data.loc[(new_data['gender'] == 'female')].index)
        return {'male':round(male/count,2),'female':round(female/count,2)}

    # Returns the number of views.
    elif kwargs['request'] == 'view':
        return count

    # Handles unidentified requests.
    else:
        return 'Unidentified request'


