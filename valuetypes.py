from couchdb.mapping import DateField, TimeField, Document, TextField

__author__ = 'bheenik'

class Appointments(Document):
    doc_type='appointment'
    date = TextField()
    time = TextField()

