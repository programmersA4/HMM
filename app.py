from flask import Flask, json, render_template, url_for, request, redirect, jsonify, make_response, send_from_directory, safe_join, abort, session
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
from requests.api import get
# from Unipose.pose_model_inference import  inference_model
import torch


import service
# from preprocess import preprocess, predict
from pred import get_pred, check_reuse

app = Flask(__name__, template_folder='Template')
cors = CORS(app)
Bootstrap(app)

app.config['image'] = '/home/ubuntu/hmm/static/images/infered'
# model = torch.hub.load('JJ-HH/yolov5', 'yolov5x')
# 핸드폰 계단 샐러드 개 고양이 
# total = torch.hub.load('taehyun-learn/yolov5', 'custom', path='yolov5m_total.pt')
# 핸드폰 과일
# fruit = torch.hub.load('taehyun-learn/yolov5', 'custom', path='yolov5m_fruit.pt')


"""
Routes
"""
@app.route('/', methods=['GET'])
def index():
    # return render_template('webcam.html')
    return render_template('main_page.html')

@app.route('/image/<path:image_name>', methods=['GET'])
def send_infered_img(image_name):
    safe_path = safe_join(app.config['image'], image_name)
    print(safe_path)
    try:
        return send_from_directory(app.config['image'], image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/capture_img', methods=['POST'])
def capture_img():
    pose = ['pullup', 'pushup', 'plank', 'squat']
    yolo = {'stairs': ['stairs'], 'walk with pet': ['cat', 'dog'], 'salad': ['salad'], 'fruit': ['fruit']}
        
    msg, im_path = service.save_img(request.form["img"])
    infered_path = "static/images/infered"
    
    print(msg, im_path)
    ch = request.form["challenge"]
    challenge = ch.replace("-", "").lower()
    print(challenge)
    result = {}

    if challenge in pose:
        from Unipose.pose_model_inference import  inference_model
        print('unipose')
        is_posture = inference_model(challenge, im_path, model_dir='Unipose/classifier')
        result['success'] = is_posture
        print('unipose infered!')
    else:
        print('yolo')
        if challenge == 'fruit': 
            fruit = torch.hub.load('taehyun-learn/yolov5', 'custom', path='yolov5m_fruit.pt')
            infered = fruit(im_path)
        else:
            total = torch.hub.load('taehyun-learn/yolov5', 'custom', path='yolov5m_total.pt')
            infered = total(im_path)
            print('yolo infered!')
    
        infered.save(save_dir='/home/ubuntu/hmm/static/images/infered')
        detected = get_pred(infered)
        
        reused = False
        mobile_detected = False
        if "mobile phone" in detected:
            reused = check_reuse(infered)
            mobile_detected = True
            # print("mobile phone Detected", end="  ")
        
        # print("reused:", reused)
        # print("chaellenge:", challenge)
        # print("target_class:", yolo.get(challenge, ""))

        if reused:
            result['success'] = False
        else:
            result['success'] = False
            for _c in yolo.get(challenge, ""):
                if _c != 'mobile phone'  and _c in detected:    
                    result['success'] = True
                    # print("_c:", _c)
                    break 
        # print("detected_objects:", detected)
        result["reused"] = reused
        result["target_class"] = yolo.get(challenge, "")
        result["detected_objects"] = detected
        result["mobile_detected"] = mobile_detected

    # url_filename = infered_path.replace("static/", "")
    filename = im_path.split('/')[-1].strip(" ")
    # print(filename)
    # print(url_for('static', filename=filename))
    result['img'] = filename
    result["chaellenge"] = challenge
    print("result:",  result)

    return make_response(jsonify(result))


# if __name__ == "__main__":
#     app.run()
    # app.run(host="0.0.0.0", port=5000)
