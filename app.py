from flask import Flask, json, render_template, url_for, request, redirect, jsonify, make_response
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
from requests.api import get
import torch


import service
# from preprocess import preprocess, predict
from pred import get_pred

app = Flask(__name__, template_folder='Template')
cors = CORS(app)
Bootstrap(app)

# model = torch.hub.load('JJ-HH/yolov5', 'yolov5x')
model = torch.hub.load('JJ-HH/yolov5', 'custom', path='yolov5m.pt')

"""
Routes
"""
@app.route('/', methods=['GET'])
def index():
    # return render_template('webcam.html')
    return render_template('main_page.html')

@app.route('/capture_img', methods=['POST'])
def capture_img():
    msg, im_file = service.save_img(request.form["img"])
    challenge = request.form["challenge"]
    # rib = preprocess(im_file[2:])
    # res = predict(rib)
    # print(res)
    infered = model(im_file[2:])
    infered.save(save_dir="static/images")
    deteced = get_pred(infered)
    deteced['img'] = url_for('static', filename=im_file[2:])
    print(deteced)
    # print(msg, im_file[2:])
    # res = model(im_file[2:])
    # l = get_pred(res)
    # print(challenge)
    # print(l)
    return make_response(jsonify(deteced))

@app.route('/sample', methods=['GET'])
def sample_api_response():
    # return jsonify(data001='DATA001')
    return render_template('album.html')


if __name__ == "__main__":
    app.run()
    # app.run(host="0.0.0.0", port=5000)
