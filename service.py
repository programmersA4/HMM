import base64
import numpy as np
import cv2
import os

from hashids import Hashids
from datetime import datetime
import secrets



def save_img(img_base64):
    image_names = [name for name in os.listdir('static/images/auth')]
    print(len(image_names), "images found")
    
    hid = Hashids()
    rand = secrets.choice(range(100, 1000))
    now = datetime.now().timestamp()
    output = hid.encode(rand, *map(int, str(now).split(".")))

    #binary <- string base64
    img_binary = base64.b64decode(img_base64)
    #jpg <- binary
    img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
    #raw image <- jpg
    img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)

    #Path to save the decoded image
    image_file=f"static/images/auth/img{output}.jpg"
    
    #Save image
    cv2.imwrite(image_file, img)
    return "SUCCESS", image_file
