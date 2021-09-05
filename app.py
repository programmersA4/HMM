from flask import Flask, json, render_template, url_for, request, redirect, jsonify, make_response
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
import service


app = Flask(__name__, template_folder='Template')
cors = CORS(app)
Bootstrap(app)

"""
Routes
"""
@app.route('/', methods=['GET'])
def index():
    # return render_template('webcam.html')
    return render_template('main_page.html')

@app.route('/capture_img', methods=['POST'])
def capture_img():
    msg = service.save_img(request.form["img"])
    return make_response(msg)

@app.route('/sample', methods=['GET'])
def sample_api_response():
    # return jsonify(data001='DATA001')
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
