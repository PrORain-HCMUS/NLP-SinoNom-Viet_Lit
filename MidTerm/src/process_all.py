"""
    Hiện tại không còn sử dụng
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import shutil

def has_chinese_characters(text):
    """Kiểm tra xem văn bản có chứa ký tự Hán không"""
    for char in text:
        # Kiểm tra range của ký tự Hán
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

def preprocess_image(image_path):
    """Tiền xử lý ảnh để cải thiện khả năng nhận dạng"""
    # Đọc ảnh bằng OpenCV
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Chuyển sang ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Tăng độ tương phản
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    contrast = clahe.apply(gray)
    
    # Khử nhiễu
    denoised = cv2.fastNlMeansDenoising(contrast)
    
    return Image.fromarray(denoised)

def check_han_nom_content(image_path):
    """Kiểm tra xem ảnh có chứa chữ Hán Nôm không"""
    try:
        # Tiền xử lý ảnh
        processed_image = preprocess_image(image_path)
        if processed_image is None:
            return False
        
        # Nhận dạng với tesseract sử dụng language pack Chinese
        text = pytesseract.image_to_string(processed_image, lang='chi_tra+chi_sim')
        
        # Kiểm tra có ký tự Hán không
        return has_chinese_characters(text)
        
    except Exception as e:
        print(f"Lỗi khi xử lý {image_path}: {str(e)}")
        return False

def filter_han_nom_images(source_folder, destination_folder):
    """Lọc và di chuyển các ảnh có chữ Hán Nôm sang thư mục mới"""
    # Tạo thư mục đích nếu chưa tồn tại
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Lấy danh sách các file ảnh
    image_files = [
        f for f in os.listdir(source_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
    ]
    
    han_nom_images = []
    other_images = []
    
    print("Bắt đầu quá trình lọc ảnh...")
    
    for image_file in image_files:
        image_path = os.path.join(source_folder, image_file)
        print(f"Đang xử lý: {image_file}")
        
        if check_han_nom_content(image_path):
            han_nom_images.append(image_file)
            # Copy ảnh sang thư mục đích
            shutil.copy2(image_path, os.path.join(destination_folder, image_file))
        else:
            other_images.append(image_file)
    
    # In thống kê
    print("\nKết quả lọc ảnh:")
    print(f"Tổng số ảnh: {len(image_files)}")
    print(f"Số ảnh có chữ Hán Nôm: {len(han_nom_images)}")
    print(f"Số ảnh không có chữ Hán Nôm: {len(other_images)}")
    
    print("\nDanh sách ảnh có chữ Hán Nôm:")
    for img in han_nom_images:
        print(f"- {img}")
    
    return han_nom_images

if __name__ == "__main__":
    SOURCE_FOLDER = "MidTerm/test_data"  # Thư mục chứa ảnh gốc
    FILTERED_FOLDER = "MidTerm/filtered_data"  # Thư mục để lưu ảnh đã lọc
    
    filtered_images = filter_han_nom_images(SOURCE_FOLDER, FILTERED_FOLDER)