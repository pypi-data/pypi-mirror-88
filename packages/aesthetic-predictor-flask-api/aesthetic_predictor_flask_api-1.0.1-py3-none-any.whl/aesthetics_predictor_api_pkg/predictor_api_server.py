import json
import os
import sys
from pathlib import Path

from flask import Flask, request

from werkzeug.middleware.proxy_fix import ProxyFix
import importlib

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

main_predictor = None
port = None


@app.route('/is_model_ready', methods=['GET'])
def is_model_ready():
    if main_predictor is None:
        return "Model not initialized.", 400
    else:
        return "Model initialized.", 200


@app.route("/predict", methods=['POST'])
def predict():
    if main_predictor is None:
        return "Model not initialized.", 400
    input_json = request.get_json()
    if input_json is not None:
        print("Received following request: " + str(input_json))
        content_path = str(input_json['contentPath'])
        start_frame = int(input_json['startFrame'])
        end_frame = int(input_json['endFrame'])
        response = main_predictor.predict(content_path, start_frame, end_frame)
        return response
    return "Error during prediction.", 400


def initialize_predictor_from_config():
    try:
        config_path = Path(os.getenv('API_CONFIG'))
        with config_path.open('r') as api_config_file:
            api_config_json = json.load(api_config_file)
            global main_predictor, port
            module = importlib.import_module(api_config_json['predictorModulePath'])
            class_ = getattr(module, api_config_json['predictorClassName'])
            main_predictor = class_()
            port = api_config_json['port']
            print("Predictor Initialized")
            return app
    except Exception as e:
        print("Could not initialize prediction api.")
        print(str(e))


def stop_api_if_init_unsuccessful():
    if main_predictor is None or port is None:
        return sys.exit()


initialize_predictor_from_config()
stop_api_if_init_unsuccessful()


if __name__ == '__main__':
    try:
        print("Starting server...")
        app.run(debug=False, threaded=True, port=port, host='0.0.0.0')
    except Exception as e:
        print("Exception Occurred!")
        print(str(e))


