class events(db.Model):
    content_id = 
    device_id = 
    event_type = db.Column(db.String(10))
    event_time =db.Column(db.DateTime) 

class persons(db.Model):
    device_id = 
    appears = db.Column(db.DateTime)
    disappears = db.Column(db.DateTime)
    age = 
    gender = db.Column(db.String(10))


