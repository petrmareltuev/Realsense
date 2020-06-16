import numpy as np
import cv2
import glob

# критерий остановки калибровки
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# мы используем шахматную доску 8x6
objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

# массивы для хранения объектов и точек всех изображений
objpoints = [] # 3d объекты из реального мира
imgpoints = [] # 2d точки на плоскости изображения

images = glob.glob('/путь_к_изображениям/*.png')

for fname in images:
img = cv2.imread(fname)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# ищем углы шахматной доски
ret, corners = cv2.findChessboardCorners(gray, (8,6),None)

# как только точки найдены, мы добавляем обновляем массивы с объектами и точками
if ret == True:
objpoints.append(objp)
corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
imgpoints.append(corners2)

# рисуем точки и показываем финальное изображение
img = cv2.drawChessboardCorners(img, (8,6), corners2,ret)
cv2.imshow('img',img)
cv2.waitKey(500)

cv2.destroyAllWindows()

# калибрируем и сохраняем результаты
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
np.save('/path_to_images/calibration', [mtx, dist, rvecs, tvecs])

# Просмотр результатов калибровки
'''
calibration_data = np.load('path_to_images/calibration.npy')
mtx = calibration_data[0]
dist = calibration_data[1]
rvecs = calibration_data[2]
tvecs = calibration_data[3]
'''