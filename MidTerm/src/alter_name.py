"""
File Name: alter_name.py
Author: Lê Hoàng Vũ
Date: 24.11
Description:
    - Script này sẽ đổi tên các file PNG trong thư mục được chỉ định bằng cách trích xuất chỉ số 
      từ tên file và chuyển nó thành định dạng 'page_XXX.png' (ví dụ: page_001.png).
Features:
    1. Quét thư mục và tìm các file PNG.
    2. Trích xuất chỉ số từ tên file và định dạng lại theo mẫu 'page_XXX.png'.
    3. Đổi tên các file thành tên mới với số thứ tự có độ dài 3 chữ số.
    4. Ghi lại quá trình đổi tên cho từng file.
Input:
    - Thư mục đầu vào (folder_path): Chứa các file PNG cần đổi tên.
Output:
    - Các file PNG được đổi tên theo định dạng 'page_XXX.png'.
Usage:
    - Đặt đường dẫn thư mục cần đổi tên vào biến `folder_path`.
    - Chạy script:
        python alter_name.py
Notes:
    - Đảm bảo thư mục chứa các file PNG với tên có chứa dấu gạch dưới và số thứ tự.
    - Các file không phải PNG sẽ bị bỏ qua.
"""


import os

# Thư mục chứa các file
folder_path = "MidTerm/data"

for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        # Trích xuất số thứ tự từ tên file
        index = int(filename.split("_")[1].split(".")[0])
        
        # Tạo tên file mới
        new_filename = f"page_{index:03d}.png"
        
        # Đổi tên file
        old_filepath = os.path.join(folder_path, filename)
        new_filepath = os.path.join(folder_path, new_filename)
        os.rename(old_filepath, new_filepath)
        print(f"Renamed {filename} to {new_filename}")