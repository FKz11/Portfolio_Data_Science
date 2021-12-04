import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired

import urllib.request


class ClientDataForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired()])
    engineSize = FloatField('Engine Size', validators=[DataRequired()])
    mpg = FloatField('Miles Per Gallon', validators=[DataRequired()])
    mileage = FloatField('Mileage', validators=[DataRequired()])
    transmission = SelectField('Transmission',
                               choices=['Manual', 'Semi-Auto', 'Automatic'],
                               validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='571dbf8e13ca219536c39ce68d435c00',
)


def get_prediction(data):
    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['year'] = int(request.form.get('year'))
        data['engineSize'] = float(request.form.get('engineSize'))
        data['mpg'] = float(request.form.get('mpg'))
        data['mileage'] = float(request.form.get('mileage'))
        data['transmission'] = request.form.get('transmission')
        try:
            response = str(get_prediction(data))
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
