def cut(frame, p1, p2):
    # 裁剪坐标为[y0:y1, x0:x1]
    cropped = frame[p1[1]:p2[1], p1[0]:p2[0]]
    return cropped
