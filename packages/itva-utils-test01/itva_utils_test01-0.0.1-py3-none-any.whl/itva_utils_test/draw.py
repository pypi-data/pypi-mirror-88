import cv2


def draw(frame, p1, p2, color, width):
    # 左上角坐标，右下角坐标，框颜色，框宽度
    cv2.rectangle(frame, p1, p2, color, width)
    return frame
