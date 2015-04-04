from flask import Flask, render_template, request, g
from emailassistant import EmailAssistant
import simplejson as json
from couchdb.design import ViewDefinition
import flaskext.couchdb
from valuetypes import Appointments

app = Flask(__name__)

__author__ = 'bheenik'

"""
CouchDB permanent view
"""
occupied_dates = ViewDefinition('times', 'occupied_times',
                                'function(doc) { if(doc.time) emit(doc.time,doc);}')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/contactus')
def contact_us_form():
    return render_template('contact.html')


@app.route('/contactus', methods=['POST'])
def contact_us_form_post():
    # Dump request in DB
    document = {'message': request.form}
    g.couch.save(document)
    email = EmailAssistant()
    email.emailer('alpha@nikitph.com', 'nikitph@gmail.com', request.form['email'], request.form['message'])
    return render_template('confirmation.html', message='Successfully sent')


@app.route('/scheduler')
def scheduler_form():
    return render_template('scheduler.html')


@app.route('/scheduler', methods=['POST'])
def scheduler_form_post():
    schedule_data = Appointments(date=request.form['date'], time=request.form['time'], name=request.form['name'],
                                 address=request.form['address'], phone=request.form['phone'],
                                 emailaddress=request.form['email'])
    id = schedule_data.store(g.couch)
    print id
    for i in occupied_dates(g.couch):
        print(json.dumps(i, sort_keys=True, indent=4 * ' '))
    body = 'Appointment confirmed for ' + request.form['name'] + ' Resident of: ' + request.form['address'] + ' on ' + \
           request.form['date'] + ' at ' + request.form['time']
    email = EmailAssistant()
    email.emailer('alpha@nikitph.com', request.form['email'], 'Your appointment confirmation from Bluddy', body)
    return render_template('confirmation.html',
                           message='Appointment confirmed for ' + request.form['name'] + ' Resident of: ' +
                                   request.form['address'] + ' on ' + request.form['date']
                                   + ' at ' + request.form['time'])


if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        COUCHDB_SERVER='http://127.0.0.1:5984/',
        COUCHDB_DATABASE='docsdemo'
    )
    manager = flaskext.couchdb.CouchDBManager()
    manager.setup(app)
    manager.add_viewdef(occupied_dates)
    manager.sync(app)
    app.run(host='127.0.0.1', port=5000)

    # TODO insert some logging in here.