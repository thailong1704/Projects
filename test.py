from ultralytics import YOLO
from PIL import Image
import cv2
import os

# Load mô hình YOLO
model = YOLO("D:\\do an\\train2\\weights\\best.pt")




results = model("C:\\Users\\ADMIN\\Downloads\\0405.mp4")

for r in results:
        print(r.boxes)  # Hiển thị bounding boxes
        im_array = r.plot()  # Vẽ kết quả lên ảnh
        im = Image.fromarray(im_array[..., ::-1])  # Chuyển đổi màu BGR -> RGB
        im.show()
        im.save('ketqua.jpg')


