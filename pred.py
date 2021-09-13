def get_pred(results):
    names = {} # class names

    for i, (im, pred) in enumerate(zip(results.imgs, results.pred)):
        img_info = f'image {i + 1}/{len(results.pred)}: {im.shape[0]}x{im.shape[1]} '
        print(img_info)

        detected_objs = dict()
        if pred.shape[0]:
            for c in pred[:, -1].unique():
                n = (pred[:, -1] == c).sum()  # detections per class
                obj = results.names[int(c)].lower()
                detected_objs[obj] = int(n)
            
            # show print confidence and bounding box
            for *box, conf, cls in reversed(pred):  # xyxy, confidence, class
                        label = f'{results.names[int(cls)]} {conf:.2f}'
                        bbox = tuple(map(float, box))
                        print(label)
    return detected_objs
