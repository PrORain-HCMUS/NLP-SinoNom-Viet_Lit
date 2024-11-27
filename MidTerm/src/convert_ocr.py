"""
File Name: convert_ocr.py
Author: Lê Hoàng Vũ
Date: 25.11.2024
Description:
    - Phiên bản cũ hơn của convert_api.py
    - Script này sử dụng Google Cloud Vision API để nhận diện văn bản từ hình ảnh.
    - Văn bản nhận diện được lọc chỉ giữ lại các ký tự Trung Quốc và được ghi vào các tệp văn bản .txt.
    - Mỗi tệp văn bản chứa các ký tự Trung Quốc và các dòng văn bản được căn chỉnh dựa trên bounding box của từng đoạn văn bản.
    - Tạo tệp txt cho mỗi ảnh, lưu kết quả vào thư mục chỉ định.
    - Xóa các tệp txt rỗng để tránh lưu trữ không cần thiết.
Features:
    1. Sử dụng Google Cloud Vision API để nhận diện văn bản trong ảnh.
    2. Lọc chỉ các ký tự Trung Quốc từ văn bản nhận diện.
    3. Xử lý văn bản và lưu kết quả vào các tệp txt tương ứng.
    4. Xử lý các ảnh trong thư mục đầu vào và lưu kết quả vào thư mục đầu ra.
    5. Tự động xóa các tệp txt rỗng sau khi xử lý.
Input:
    - Thư mục chứa ảnh (input_folder): Chứa các ảnh định dạng .png, .jpg, .jpeg.
Output:
    - Thư mục lưu kết quả (output_folder): Chứa các tệp .txt với kết quả nhận diện văn bản từ ảnh.
Usage:
    - Cài đặt Google Cloud Vision API và cung cấp tệp key.json.
    - Định nghĩa đường dẫn `input_folder` và `output_folder`.
    - Chạy script:
        python convert_ocr.py
Notes:
    - Đảm bảo đã thiết lập Google Cloud Vision API và file key.json chính xác.
    - Script này có thể xử lý nhiều ảnh trong thư mục cùng lúc và lưu kết quả cho từng ảnh vào tệp txt.
    - Các tệp txt sẽ chứa văn bản Trung Quốc được nhận diện, mỗi dòng văn bản tách biệt bởi khoảng cách bounding box.
    - Tệp txt sẽ bị xóa nếu không chứa bất kỳ văn bản nào sau khi xử lý.
"""


import os
from google.cloud import vision
from google.oauth2 import service_account

# Đường dẫn tới file key.json của bạn
key_path = "api/key.json"

# Thiết lập thông tin xác thực từ file key.json
credentials = service_account.Credentials.from_service_account_file(key_path)

# Khởi tạo client Vision API với thông tin xác thực
client = vision.ImageAnnotatorClient(credentials=credentials)

# Hàm kiểm tra xem một ký tự có phải là ký tự Trung Quốc không
def is_chinese_character(char):
    return '\u4e00' <= char <= '\u9fff'

# Hàm lọc văn bản chỉ giữ lại ký tự Trung Quốc
def filter_chinese_text(text):
    return ''.join(char for char in text if is_chinese_character(char))

# Hàm nhận diện văn bản từ hình ảnh
def detect_text(path):
    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

# Hàm để xử lý tất cả các ảnh trong folder và lưu kết quả vào thư mục output
def ocr_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Kiểm tra xem có phải file hình ảnh không
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing {filename}...")

            # Nhận diện văn bản
            texts = detect_text(file_path)

            # Tạo tên tệp txt tương ứng
            output_txt_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")

            # Ghi kết quả vào tệp txt
            with open(output_txt_path, "w", encoding="utf-8") as output_file:
                last_bottom = None
                current_line = []

                for text in texts[1:]:  # Bỏ qua phần tử đầu tiên (toàn bộ văn bản)
                    chinese_text = filter_chinese_text(text.description)
                    
                    if chinese_text:
                        # Lấy vị trí bounding box của văn bản
                        vertices = text.bounding_poly.vertices
                        top = vertices[0].y
                        bottom = vertices[2].y
                        
                        # Nếu có khoảng cách lớn giữa các dòng, tạo một dòng mới
                        if last_bottom and top - last_bottom > 10:
                            output_file.write("".join(current_line) + "\n")
                            current_line = []

                        # Thêm văn bản vào dòng hiện tại
                        current_line.append(chinese_text)

                        last_bottom = bottom

                # Ghi lại dòng cuối cùng
                if current_line:
                    output_file.write("".join(current_line) + "\n")
            
            # Kiểm tra xem tệp văn bản có rỗng không
            if os.path.getsize(output_txt_path) == 0:
                os.remove(output_txt_path)  # Xóa tệp nếu không có nội dung
                print(f"Removed empty file: {output_txt_path}")
            else:
                print(f"Results saved to {output_txt_path}")

# Đường dẫn thư mục đầu vào và đầu ra
input_folder = "MidTerm/data"  # Thư mục chứa ảnh
output_folder = "MidTerm/output"    # Thư mục lưu kết quả

# Gọi hàm để xử lý các ảnh trong thư mục đầu vào và lưu kết quả vào thư mục output
ocr_images_in_folder(input_folder, output_folder)
