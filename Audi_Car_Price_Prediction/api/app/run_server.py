# import the necessary packages
import dill
import pandas as pd
import numpy as np
import os

dill._dill._reverse_typemap['ClassType'] = type
# import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    # load the pre-trained model
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    print(model)
    return model


# initialize our Flask application and the model
app = flask.Flask(__name__)
model_path = "/app/app/models/xgb_pipeline.dill"
model = load_model(model_path)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to audi car price prediction process. Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":

        request_json = flask.request.get_json()
        params = ['year', 'engineSize', 'mpg', 'mileage', 'transmission']
        dict_params = dict()
        for param in params:
            dict_params[param] = request_json[param]
        try:
            preds = model.predict(pd.DataFrame(dict_params, index=[0]))
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = str(preds[0])
        # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    print(data)
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    app.run(host='0.0.0.0', debug=True, port=8180)
