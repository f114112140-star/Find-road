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
``` python
h, w = img.shape[:2]
roi_y = int(h * 0.45)
roi = img[roi_y:, :]
```
