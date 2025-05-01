from mongoengine import  connect

def connect_mongo():
    connect(
        db='meet_data',
        host='localhost',
        port=27017
    )