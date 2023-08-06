#!/usr/bin/python3

import peewee
from peewee import DateTimeField, TextField, DecimalField, IntegerField
from playhouse.db_url import connect

db = peewee.DatabaseProxy()

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Temperature(BaseModel):
    timestamp = DateTimeField(index=True)
    name = TextField()
    location = TextField()
    environment = TextField()
    source = TextField()
    temp = DecimalField()
    json = TextField(null=False)

    class Meta:
        indexes = (
            (('timestamp', 'name'), True),
        )

class Humidity(BaseModel):
    timestamp = DateTimeField(index=True)
    name = TextField()
    location = TextField()
    environment = TextField()
    source = TextField()
    humidity = DecimalField()
    json = TextField(null=False)

    class Meta:
        indexes = (
            (('timestamp', 'humidity'), True),
        )

class Sensor(BaseModel):
    name = TextField()
    sensortype = TextField()
    host = TextField()
    comment = TextField()
    created = DateTimeField()

def create_tables(uri):
    db.initialize(connect(uri))
    with db:
        db.create_tables([Temps])
