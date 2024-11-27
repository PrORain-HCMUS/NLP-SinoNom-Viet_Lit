"""
File Name: filter_img.py
Author: Lê Hoàng Vũ
Date: 24.11.2024
Description:
    - Script này lọc các ảnh từ thư mục `data_folder` dựa trên sự tồn tại của các tệp văn bản tương ứng trong thư mục `output_folder`.
    - Các ảnh có tên phù hợp với các tệp văn bản sẽ được sao chép vào thư mục `filtered_data_folder`.
    - Tên tệp ảnh và tệp văn bản được xác định dựa trên số thứ tự trong tên tệp ảnh.
Features:
    1. Lọc ảnh từ thư mục `data_folder` dựa trên các tệp văn bản trong thư mục `output_folder`.
    2. Các ảnh có tên trùng khớp với tệp văn bản sẽ được sao chép vào thư mục `filtered_data_folder`.
    3. Tạo thư mục `filtered_data_folder` nếu chưa tồn tại.
Input:
    - Thư mục chứa các ảnh (data_folder): Chứa các tệp ảnh .png.
    - Thư mục chứa các tệp văn bản (output_folder): Chứa các tệp .txt tương ứng với ảnh.
Output:
    - Thư mục đầu ra (filtered_data_folder): Lưu các ảnh đã lọc và sao chép.
Usage:
    - Đặt đường dẫn thư mục chứa ảnh vào biến `data_folder` và thư mục chứa tệp văn bản vào biến `output_folder`.
    - Chạy script:
        python filter_img.py
Notes:
    - Tệp ảnh phải có định dạng .png và tên có chứa số thứ tự (ví dụ: page_001.png).
    - Chỉ những ảnh có tệp văn bản tương ứng mới được sao chép vào thư mục đầu ra.
"""


import os
import shutil

# Thư mục chứa các file ảnh
data_folder = "MidTerm/data"
# Thư mục chứa các file tên
output_folder = "MidTerm/output"
# Thư mục để lưu ảnh đã được lọc
filtered_data_folder = "MidTerm/filtered_data"

# Tạo thư mục filtered_data nếu chưa tồn tại
if not os.path.exists(filtered_data_folder):
    os.makedirs(filtered_data_folder)

# Lấy danh sách các file tên trong thư mục output
output_files = [f for f in os.listdir(output_folder) if f.endswith(".txt")]

for filename in os.listdir(data_folder):
    if filename.endswith(".png"):
        # Trích xuất số thứ tự từ tên file
        index = int(filename.split("_")[1].split(".")[0])
        
        # Tạo tên file tên tương ứng
        output_filename = f"page_{index:03d}.txt"
        
        # Kiểm tra xem file tên có tồn tại trong thư mục output không
        if output_filename in output_files:
            # Copy file ảnh vào thư mục filtered_data
            src_path = os.path.join(data_folder, filename)
            dst_path = os.path.join(filtered_data_folder, filename)
            shutil.copy(src_path, dst_path)
            print(f"Copied {filename} to {filtered_data_folder}")