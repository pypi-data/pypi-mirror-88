import numpy
import cv2


def cut_poly(frame, points):
    b = [numpy.array(points, dtype=numpy.int32)]
    num_x = []
    num_y = []
    for point in points:
        num_x.append(point[0])
        num_y.append(point[1])
    max_x = max(num_x)
    max_y = max(num_y)
    min_x = min(num_x)
    min_y = min(num_y)
    # 创建一个和原图一样的全0数组
    img_zero = numpy.zeros(frame.shape[:2], dtype="uint8")
    cv2.polylines(img_zero, b, 1, 255)
    cv2.fillPoly(img_zero, b, 255)
    mask = img_zero
    # 将连接起来的区域对应的数组和原图对应位置按位相与
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    cropped = masked[min_y:max_y, min_x:max_x]
    return cropped


