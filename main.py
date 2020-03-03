import os
import base64
import peewee

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor 

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            donor = Donor.get(Donor.name == request.form['donor'])
        except peewee.DoesNotExist:
            return render_template('create.jinja2', error='Existing donor not found')

        Donation(donor = donor, value=request.form['value']).save()
        return redirect(url_for('all'))
    else:
        return render_template('create.jinja2')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

