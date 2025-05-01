# models.py

from mongoengine import Document, StringField, FileField, connect

class MeetSpace(Document):
    space_name = StringField(required=True, unique=True)
    topic_name = StringField(required=True)
    space_uri = StringField(required=True)

    # Optional fields for transcript and recording files
    transcript = FileField()  # Use .put() with a text file
    recording = FileField()  # Use .put() with an audio file

    meta = {
        'collection': 'meet_spaces',
        'indexes': ['space_name']
    }