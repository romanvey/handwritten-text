from flask import Flask, render_template, request, jsonify

application = Flask(__name__)


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

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)