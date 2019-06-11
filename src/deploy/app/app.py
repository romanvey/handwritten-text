import yaml
import json
from http import HTTPStatus
from flask import Flask, render_template, request, Response,  jsonify
from contrib.generate import HWGenerator

application = Flask(__name__)

with open("config.yaml", "r") as f:
    config = yaml.load(f)
model = HWGenerator(config["model"])


@application.route("/")
def index():
    return render_template("index.html")


@application.route('/api', methods=['POST'])
def api():
    try:
        body = request.get_json()
        svg_img = model.plot_text(body["text"], style=int(body["style"]), bias=float(body["bias"]))
        return create_json_response(response={"img": svg_img}, status=HTTPStatus.OK)
    except Exception as e:
        return create_json_response(response=str(e), status=HTTPStatus.BAD_REQUEST)


def create_json_response(status, response):
    response = Response(response=json.dumps(response), status=status, mimetype='application/json')
    return response


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)
