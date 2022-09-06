import string

import cv2
from PIL import Image

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV

        ret, jpeg = cv2.imencode('.jpg', frame)
        img = Image.fromarray(frame, "RGB")

        detector = cv2.QRCodeDetector()
        print("IMENCODE RET:" + str(jpeg))
        data, vertices_array, binary_qrcode = detector.detectAndDecode(frame)
        print("QRCode data:")
        print(data)

        return jpeg.toByte
