import pandas as pd
import sqlite3
import os
import sys

if os.path.exists('advertima.db'):
    print('Database already exists !!')
    sys.exit()
if not os.path.exists('events.csv'):
    events_csv = input('Provide full path to events.csv eg:/path/to/events.csv\n').strip()
else:
    events_csv = 'events.csv'
if not os.path.exists('persons.csv'):
    persons_csv = input('Provide full path to persons.csv eg:/path/to/persons.csv\n').strip()
else:
    persons_csv = 'persons.csv'

print('Reading events.csv')
data = pd.read_csv(events_csv)
data['event_time']=pd.to_datetime(data['event_time'])

print('Sorting events.csv')

# Create separate dataframes for event start and event end rows, sort them by content_ID, device_ID and time.
df_start = data[data['event_type'] == 'start'].sort_values(by=['content_ID','device_ID','event_time'])
df_end = data[data['event_type'] == 'end'].sort_values(by=['content_ID','device_ID','event_time'])
df_start = df_start.reset_index(drop=True)
df_end = df_end.reset_index(drop=True)

# Add an index column Renaming and dropping duplicate columns.
df_start['event_id'] = df_start.index
df_start['start_time'] = df_start['event_time']
df_end['end_time']=df_end['event_time']
df_start = df_start.drop(["event_type","event_time"], axis=1)
df_end = df_end.drop(["event_type","event_time","content_ID","device_ID"],axis=1)

# Merge start and end dataframe
merged = pd.concat([df_start,df_end],axis =1)

print('Writing %s to database' %(events_csv))
# If the file does not exist new file will be created.
try:
    conn = sqlite3.connect('advertima.db')
except IOError:
    db_file = input('Please provide full path to create database /path/to/advertima.db').strip()
    conn = sqlite3.connect(db_file)
cur = conn.cursor()
merged.to_sql(name="event", con=conn, if_exists="append", index=False)

print('Reading persons.csv')
person = pd.read_csv(persons_csv)
person['id']=person.index
person['appears'] = pd.to_datetime(person['appears'])
person['disappears'] = pd.to_datetime(person['disappears'])
person = person.sort_values(by=['device_id','appears'])
person.head()
print('Writing %s to database' %(persons_csv))
person.to_sql(name="person", con=conn, if_exists="append", index=False)

print('Indexing events table on content id')
sql = "CREATE INDEX content_idx ON event (content_ID);"
cur.execute(sql)

print('Indexing persons table on device_id')
sql = "CREATE INDEX pdevice_idx ON person (device_id);"
cur.execute(sql)

print('Database ready !!')

