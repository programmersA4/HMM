import base64
import numpy as np
import cv2
import os


image_names = [name for name in os.listdir('static/images/auth')]
current_id = len(image_names)
print(current_id, image_names)

def save_img(img_base64):
    global current_id
    #binary <- string base64
    img_binary = base64.b64decode(img_base64)
    #jpg <- binary
    img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
    #raw image <- jpg
    img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)

    #Path to save the decoded image
    current_id += 1
    image_file=f"static/images/auth/img{current_id:04}.jpg"
    print(current_id)
    #Save image
    cv2.imwrite(image_file, img)
    return "SUCCESS", image_file
