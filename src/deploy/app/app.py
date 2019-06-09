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


@application.route('/get_text', methods=['POST'])
def get_text():
    request_data = request.get_json()
    if request.method == 'POST':
        text = "haha"
        style = "style"
    img = generate_hw_text(text, style)
    response = jsonify({'img_link':img})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
    return response

def generate_hw_text(text, style):
    link = "https://txt.static.1001fonts.net/txt/dHRmLjcyLjAwMDAwMC5RWFIwWVdOcklHOW1JSFJvWlNCRGRXTjFiV0psY25NLC4w/attack-of-the-cucumbers.regular.png"
    return link

@application.route('/api', methods=['POST'])
def api():
    body = request.get_json()
    try:
        svg_img = model.plot_text(body["text"], style=body["style"])
        return create_json_response(response={"img": svg_img}, status=HTTPStatus.OK)
    except Exception as e:
        return create_json_response(response=str(e), status=HTTPStatus.BAD_REQUEST)


def create_json_response(status, response):
    return Response(response=json.dumps(response), status=status, mimetype='application/json')


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)
