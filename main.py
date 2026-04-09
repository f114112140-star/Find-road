import cv2
import numpy as np
from collections import deque

img_path = r"C:\Users\user\Desktop\Find-road\images\002.jpg"

data = np.fromfile(img_path, dtype=np.uint8)
img = cv2.imdecode(data, cv2.IMREAD_COLOR)

if img is None:
    print("圖片讀取失敗")
    exit()

h, w = img.shape[:2]
roi_y = int(h * 0.45)
roi = img[roi_y:, :]

gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

rh, rw = gray.shape

# 種子點：下半部中央偏下
seed_x = rw // 2
seed_y = int(rh * 0.9)

seed_val = int(gray[seed_y, seed_x])

visited = np.zeros((rh, rw), dtype=np.uint8)
mask_roi = np.zeros((rh, rw), dtype=np.uint8)

q = deque()
q.append((seed_y, seed_x))
visited[seed_y, seed_x] = 1

threshold = 20  # 與種子灰階差容許值，可調

directions = [(-1,0),(1,0),(0,-1),(0,1)]

while q:
    y, x = q.popleft()
    cur_val = int(gray[y, x])

    if abs(cur_val - seed_val) <= threshold:
        mask_roi[y, x] = 255

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rh and 0 <= nx < rw and visited[ny, nx] == 0:
                visited[ny, nx] = 1
                q.append((ny, nx))

# 後處理
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
mask_roi = cv2.morphologyEx(mask_roi, cv2.MORPH_CLOSE, kernel, iterations=2)

mask = np.zeros((h, w), dtype=np.uint8)
mask[roi_y:, :] = mask_roi

result = img.copy()
overlay = result.copy()
overlay[mask == 255] = (0, 255, 0)
final = cv2.addWeighted(overlay, 0.4, result, 0.6, 0)

cv2.imshow("Gray ROI", gray)
cv2.imshow("Road Mask BFS", mask)
cv2.imshow("Final", final)
cv2.waitKey(0)
cv2.destroyAllWindows()