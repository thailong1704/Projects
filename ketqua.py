
from PIL import Image
from ultralytics import YOLO

# Load mô hình YOLO
model = YOLO("D:\\do an\\train2\\weights\\best.pt")

# Đường dẫn đầu vào
input_path ="C:\\Users\\ADMIN\\Downloads\\images.jpg"
if input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
    # Chạy dự đoán trên video
    results = model.predict(source=input_path, save=True)
    

else:
    results = model(input_path)
    for r in results:
        print(r.boxes)  # Hiển thị bounding boxes
        im_array = r.plot()  # Vẽ kết quả lên ảnh
        im = Image.fromarray (im_array[..., ::-1])  # Chuyển đổi màu BGR -> RGB
        im.show()
        im.save('ketqua.jpg')


