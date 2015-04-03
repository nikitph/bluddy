from flask import Flask, render_template, request, g
from emailassistant import EmailAssistant
import simplejson as json
from couchdb.design import ViewDefinition
import flaskext.couchdb
from datetime import datetime
from valuetypes import Appointments
import strftime

app = Flask(__name__)

from couchdb.mapping import DateField, TimeField, Document

__author__ = 'bheenik'



"""
CouchDB permanent view
"""
occupied_dates = ViewDefinition('times', 'occupied_times',
                                'function(doc) { if(doc.time) emit(doc.time);}')



@app.route('/')
def hello_world():
    email = EmailAssistant()
    email.emailer('alpha@nikitph.com', 'nikitph@gmail.com', 'test', 'test')
    return 'Hello World!'


@app.route('/contactus')
def contact_us_form():
    return render_template('contact.html')


@app.route('/contactus', methods=['POST'])
def contact_us_form_post():
    # Dump request in DB
    document = {'message': request.form}
    g.couch['1'] = document
    email = EmailAssistant()
    email.emailer('alpha@nikitph.com', 'nikitph@gmail.com', request.form['email'], request.form['message'])
    return render_template('confirmation.html', message='Successfully sent')


@app.route('/scheduler')
def scheduler_form():
    return render_template('scheduler.html')


@app.route('/scheduler', methods=['POST'])
def scheduler_form_post():

    schedule_data = Appointments(date = request.form['date'], time = request.form['time'])
    id = schedule_data.store(g.couch)
    for i in occupied_dates(g.couch):
        print(json.dumps(i, sort_keys=True, indent=4 * ' '))
    email = EmailAssistant()
    email.emailer('alpha@nikitph.com', 'nikitph@gmail.com', request.form['date'], request.form['time'])
    return render_template('scheduler.html')


if __name__ == "__main__":
    app.config.update(
        DEBUG = True,
        COUCHDB_SERVER = 'http://127.0.0.1:5984/',
        COUCHDB_DATABASE = 'docsdemo'
    )
    manager = flaskext.couchdb.CouchDBManager()
    manager.setup(app)
    manager.add_viewdef(occupied_dates)
    manager.sync(app)
    app.run(host='127.0.0.1', port=5000)

    # TODO insert some logging in here.