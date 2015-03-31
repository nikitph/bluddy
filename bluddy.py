from flask import Flask, render_template, request
from emailassistant import EmailAssistant

app = Flask(__name__)


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
    email = EmailAssistant()
    email.emailer('alpha@nikitph.com', 'nikitph@gmail.com', request.form['email'], request.form['message'])
    return render_template('confirmation.html', message='Successfully sent')



if __name__ == '__main__':
    app.run()
