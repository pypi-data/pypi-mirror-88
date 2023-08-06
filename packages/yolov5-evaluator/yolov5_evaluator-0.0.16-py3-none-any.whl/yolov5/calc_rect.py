import cv2
import numpy as np

# 填充目标区域padding像素
def padRect(image, box, padding):
    height, width, num = image.shape

    x, y, w, h = box
    y0, y1, x0, x1 = y-padding, y+h+padding, x-padding, x+w+padding

    if(y0 < 0):
        y0 = 0
    if(y1 > height):
        y1 = height
    if(x0 < 0):
        x0 = 0
    if(x1 > width):
        x1 = width
    return (int(x0), int(y0), int(x1), int(y1))


# 精确计算目标区域
def calcRect(image, box, padding=20, areaThreshold=900):

    # 放到目标区域
    x0, y0, x1, y1 = padRect(image, box, padding)
    img = image[y0:y1, x0:x1]

    # 灰度
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 高斯模糊
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Canny提取边缘
    processed = cv2.Canny(img, 50, 150, 1)

    # 寻找轮廓
    contours, hierarchy = cv2.findContours(
        processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if(len(contours) <= 0):
        return None

    # 根据面积过滤，筛选大面积的框
    maxAreas = list(filter(lambda cons: cv2.contourArea(cons)
                           > areaThreshold, contours))

    if(len(maxAreas) <= 0):
        return None

    # 获取点的矩形
    rects = list(map(lambda area: cv2.minAreaRect(area), maxAreas))

    if(len(rects) <= 0):
        return None

    # 矩形数据结构转换成数组
    rectArr = list(map(lambda rect: [int(rect[0][0]-rect[1][0]/2+x0), int(
        rect[0][1]-rect[1][1]/2+y0), int(rect[1][0]), int(rect[1][1])], rects))

    # 获取最大的矩形
    result = max(rectArr, key=lambda rect: rect[2]*rect[3])

    return result


def calcRectByImage(image, boxs=[], padding=20, areaThreshold=900):
    arr = np.asarray(bytearray(image), dtype="uint8")
    img0 = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    results = []
    for box in boxs:
        label, x, y, w, h = box
        result = calcRect(img0, [x, y, w, h], padding, areaThreshold)
        if(result != None):
            results.append([label, result[0], result[1], result[2], result[3]])
        else:
            results.append(box)

    return results
