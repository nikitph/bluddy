from couchdb.mapping import Document, TextField

__author__ = 'bheenik'

class Appointments(Document):
    doc_type = 'appointment'
    date = TextField()
    time = TextField()
    name = TextField()
    address = TextField()
    phone = TextField()
    emailaddress = TextField()

