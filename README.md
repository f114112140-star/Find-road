# 找馬路

## 專案流程
讀取圖片 → 取道路可能區域(ROI) → 灰階與模糊 → 用 BFS 從種子點長出相似區域 → 形態學補洞 → 疊回原圖顯示

### 讀取圖片
``` python 
img_path = r"C:\Users\user\Desktop\Find-road\images\002.jpg"

data = np.fromfile(img_path, dtype=np.uint8)
img = cv2.imdecode(data, cv2.IMREAD_COLOR)
```
### 取得影像大小，切出ROI
因為馬路通常是在下方所以從影像高度的45%往下取，保留下半部區域
``` python
h, w = img.shape[:2]
roi_y = int(h * 0.45)
roi = img[roi_y:, :]
```
### 灰階與高斯模糊
將彩色圖轉灰階，方便比較像素亮度 
用高斯模糊把小雜訊去掉
``` python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
```
### 設定種子點 seeed
設定BFS的起始點，ROI水平中間，靠近底部90%位置
``` python
seed_x = rw // 2
seed_y = int(rh * 0.9)
```
### 後處理:形態學closing
用closing填補小洞，連接斷裂區域，讓道路更完整
``` python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
mask_roi = cv2.morphologyEx(mask_roi, cv2.MORPH_CLOSE, kernel, iterations=2)
```
## 成果展示
後處理kernel變化
```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
```
<img width="803" height="605" alt="image" src="https://github.com/user-attachments/assets/b17e1bae-c802-4709-b64b-d0a93d0238d8" />
```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
```
<img width="798" height="601" alt="image" src="https://github.com/user-attachments/assets/9b1215b8-cf53-4499-8f56-04d55026cc3c" />
