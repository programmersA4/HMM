def get_pred(results):
    for i, (im, pred) in enumerate(zip(results.imgs, results.pred)):
        str = f'image {i + 1}/{len(results.pred)}: {im.shape[0]}x{im.shape[1]} '
        if pred.shape[0]:
            for c in pred[:, -1].unique():
                n = (pred[:, -1] == c).sum()  # detections per class
                str += f"{n} {results.names[int(c)]}{'s' * (n > 1)}, "  # add to string
            # if show or save or render or crop:
            #     annotator = Annotator(im, pil=not results.ascii)
            #     for *box, conf, cls in reversed(pred):  # xyxy, confidence, class
            #         label = f'{results.names[int(cls)]} {conf:.2f}'
            #         if crop:
            #             save_one_box(box, im, file=save_dir / 'crops' / results.names[int(cls)] / results.files[i])
            #         else:  # all others
            #             annotator.box_label(box, label, color=colors(cls))
            #     im = annotator.im
        else:
            str += '(no detections)'
    return str
