import pickle
from flask import Flask, render_template, request
import os
from random import random
from my_yolov7 import detect
import cv2

# Khởi tạo Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static"

# Hàm xử lý request
@app.route("/", methods=['GET', 'POST'])
def home_page():
    # Nếu là POST (gửi file)
    if request.method == "POST":
#          try:
            # Lấy file gửi lên
            image = request.files['file']
            if image:
                # Lưu file
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                print("Save = ", path_to_save)
                image.save(path_to_save)

                # Convert image to dest size tensor
                frame = path_to_save

                frame = detect(frame,"weights/last.pt","yolov7/data/mydataset.yaml")

                cv2.imwrite(path_to_save, frame)

                # Trả về kết quả
                return render_template("index.html", user_image = image.filename , rand = str(random()),
                                           msg="Tải file lên thành công")
            else:
                # Nếu không có file thì yêu cầu tải file
                return render_template('index.html', msg='Hãy chọn file để tải lên')

#          except Exception as ex:
#             # Nếu lỗi thì thông báo
#             print(ex)
#             return render_template('index.html', msg='Không nhận diện được vật thể')

    else:
        # Nếu là GET thì hiển thị giao diện upload
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)