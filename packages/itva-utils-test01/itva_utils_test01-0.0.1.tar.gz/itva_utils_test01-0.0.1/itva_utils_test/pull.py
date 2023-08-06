import cv2


def pull(t, ip, usr, pwd):
    cap = cv2.VideoCapture("rtsp://%s:%s@%s" % (usr, pwd, ip))
