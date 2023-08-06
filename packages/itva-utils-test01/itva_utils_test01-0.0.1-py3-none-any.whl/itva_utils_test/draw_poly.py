import cv2
import numpy


def drawpoly(frame, points, color):
    pts = numpy.array(points, numpy.int32)
    pts = pts.reshape(-1, 1)
    # 按照点的顺序逆时针绘制，如果给的点不正确，会出现边交叉等情况
    cv2.polylines(frame, [pts], True, color)
    return frame


a = [100, 100]
b = [50, 300]
c = [200, 250]
d = [100, 200]
e = [150, 150]
points1 = [[a, b, c, d, e]]
