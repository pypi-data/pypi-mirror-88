from mongoengine import (
    Document, EmbeddedDocument, fields
)


class EventLivePPT(Document):
    event_id = fields.StringField(max_length=32)
    image_list = fields.ListField(fields.StringField())

    meta = {'collections': 'event_live_ppt'}
