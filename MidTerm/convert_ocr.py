import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os
import shutil
import re

# Đặt đường dẫn đến Tesseract executable
TESSERACT_CMD = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def preprocess_image(image_path: str):
    """Tiền xử lý ảnh để cải thiện chất lượng nhận dạng"""
    try:
        # Đọc ảnh bằng PIL
        image = Image.open(image_path)
        # Chuyển sang ảnh xám
        image = image.convert('L')
        
        # Tăng độ tương phản
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        
        # Làm sắc nét ảnh
        image = image.filter(ImageFilter.SHARPEN)
        
        # Chuyển sang numpy array để xử lý với OpenCV
        image_np = np.array(image)
        
        # Khử nhiễu
        image_denoised = cv2.fastNlMeansDenoising(image_np, h=10)
        
        # Ngưỡng hóa thích ứng
        image_thresh = cv2.adaptiveThreshold(
            image_denoised, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            11, 
            2
        )
        
        return Image.fromarray(image_thresh)
        
    except Exception as e:
        print(f"Lỗi khi tiền xử lý ảnh {image_path}: {str(e)}")
        return None

def count_chinese_chars(text: str) -> int:
    """Đếm số ký tự Hán trong văn bản"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def has_chinese_text(text: str) -> bool:
    """Kiểm tra xem văn bản có chứa đủ số lượng ký tự Hán không"""
    # Đếm số ký tự Hán
    chinese_count = count_chinese_chars(text)
    # Yêu cầu ít nhất 5 ký tự Hán
    return chinese_count >= 5

def debug_ocr(image_path: str, debug_folder: str = "debug_ocr"):
    """Thực hiện OCR và lưu kết quả để debug"""
    try:
        # Tạo thư mục debug nếu chưa tồn tại
        if not os.path.exists(debug_folder):
            os.makedirs(debug_folder)
            
        # Xử lý ảnh
        processed_image = preprocess_image(image_path)
        if processed_image is None:
            return False
            
        # Cấu hình OCR
        custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
        
        # Thực hiện OCR với từng ngôn ngữ riêng biệt
        results = {
            'chi_tra': pytesseract.image_to_string(processed_image, lang='chi_tra', config=custom_config),
            'chi_sim': pytesseract.image_to_string(processed_image, lang='chi_sim', config=custom_config),
            'combined': pytesseract.image_to_string(processed_image, lang='chi_tra+chi_sim', config=custom_config)
        }
        
        # Lưu kết quả debug
        image_name = os.path.basename(image_path)
        debug_file = os.path.join(debug_folder, f"{image_name}_ocr_debug.txt")
        
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(f"Debug OCR kết quả cho {image_name}\n")
            f.write("=" * 50 + "\n\n")
            
            for lang, text in results.items():
                f.write(f"Language: {lang}\n")
                f.write("-" * 30 + "\n")
                f.write(text + "\n")
                f.write(f"Số ký tự Hán: {count_chinese_chars(text)}\n\n")
        
        # Kiểm tra có chữ Hán trong bất kỳ kết quả nào
        return any(has_chinese_text(text) for text in results.values())
        
    except Exception as e:
        print(f"Lỗi khi debug OCR {image_path}: {str(e)}")
        return False

def filter_text_images(source_folder: str, destination_folder: str):
    """Lọc và di chuyển các ảnh có chữ Hán sang thư mục mới"""
    # Tạo thư mục đích nếu chưa tồn tại
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Lấy danh sách các file ảnh
    image_files = [
        f for f in os.listdir(source_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
    ]
    
    text_images = []
    other_images = []
    
    print("Bắt đầu quá trình lọc ảnh...\n")
    
    for image_file in image_files:
        image_path = os.path.join(source_folder, image_file)
        print(f"Đang xử lý: {image_file}")
        
        # Thực hiện OCR với debug
        if debug_ocr(image_path):
            text_images.append(image_file)
            print(f"→ Phát hiện chữ Hán trong {image_file}")
            # Copy ảnh sang thư mục đích
            shutil.copy2(image_path, os.path.join(destination_folder, image_file))
        else:
            other_images.append(image_file)
            print(f"→ Không phát hiện chữ Hán trong {image_file}")
        print("-" * 50)
    
    # In thống kê
    print("\nKết quả lọc ảnh:")
    print(f"Tổng số ảnh: {len(image_files)}")
    print(f"Số ảnh có chữ Hán: {len(text_images)}")
    print(f"Số ảnh không có chữ Hán: {len(other_images)}")
    
    print("\nDanh sách ảnh có chữ Hán:")
    for img in text_images:
        print(f"- {img}")
    
    return text_images

if __name__ == "__main__":
    SOURCE_FOLDER = "MidTerm/test_data"  # Thư mục chứa ảnh gốc
    FILTERED_FOLDER = "MidTerm/filtered_data"  # Thư mục để lưu ảnh đã lọc
    
    filtered_images = filter_text_images(SOURCE_FOLDER, FILTERED_FOLDER)