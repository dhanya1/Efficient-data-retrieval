# First time run instructions.

1. Create a virtual environment.

virtualenv venv
source vnev/bin/activate

2. git clone https://github.com/dhanya1/advertima.git
3. cd advertima
4. Check permissions of all executables and fix it.
5. pip install -r requirements.txt
6. python create_database.py

This will create a advertima.db file in current folder (sqlite3 db)

7. Optionally, after database creation you can look at data_transformation notebook to visualize the data transformation.

# Repeated runs.
6. python app.py 

This will start the flask server.

7. Submit the GET requests from your local machine.

Sample URLS:

Working URLS:

http://127.0.0.1:5000/viewer-count?start_time=2016-01-29%2000:00:00&end_time=2016-01-31%2000:00:00&device_id=3&content_id=87


http://127.0.0.1:5000/viewer-count?start_time=2016-01-28%2000:00:00&end_time=2016-01-31%2000:00:00&device_id=3&content_id=40

BAD URLS:

http://127.0.0.1:5000/gender-dist?start_time=2016-01-01%2000:00:00&end_time=2016-01-31%2001:00:00&device_id=3&content_id=yu

http://127.0.0.1:5000/gender-dist?start_time=0i-01-01%2000:00:00&end_time=2016-01-31%2001:00:00&device_id=3&content_id=4
