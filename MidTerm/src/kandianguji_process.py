"""
File Name: kandianguji_process.py
Author: Lê Hoàng Vũ
Date: 24.11.2024
Description:
    - Script này sử dụng API Kandianguji OCR để nhận diện văn bản từ các hình ảnh trong thư mục.
    - Ảnh được mã hóa thành chuỗi base64 và gửi qua API để nhận diện văn bản.
    - Kết quả nhận diện được lưu dưới dạng JSON, bao gồm thông tin về trạng thái phản hồi và kết quả trả về từ API.
    - Hỗ trợ xử lý ảnh song song với `ThreadPoolExecutor` để tăng tốc độ.
    - Tổng kết và thống kê kết quả sẽ được lưu vào một file `summary.json`.
Features:
    1. Đọc và mã hóa ảnh thành base64.
    2. Gửi yêu cầu đến API OCR để nhận diện văn bản.
    3. Lưu kết quả trả về từ API dưới dạng file JSON cho từng ảnh.
    4. Xử lý song song các ảnh để tăng hiệu suất sử dụng.
    5. Lưu tổng kết quá trình xử lý vào file `summary.json`.
Input:
    - Thư mục chứa ảnh (IMAGE_FOLDER): Chứa các ảnh có định dạng .png, .jpg, .jpeg, .gif, .bmp.
    - Thư mục lưu kết quả (RESULT_FOLDER): Lưu các kết quả JSON cho từng ảnh và tổng kết.
Output:
    - Thư mục lưu kết quả (RESULT_FOLDER): Lưu kết quả cho từng ảnh và tổng kết vào các tệp JSON.
Usage:
    - Cung cấp file cấu hình `api/kdk.json` để cấu hình API.
    - Đặt đường dẫn thư mục chứa ảnh vào biến `IMAGE_FOLDER` và thư mục lưu kết quả vào biến `RESULT_FOLDER`.
    - Chạy script:
        python kandianguji_process.py
Notes:
    - Đảm bảo đã cung cấp file cấu hình `kdk.json` với thông tin cần thiết.
    - Thư mục `RESULT_FOLDER` sẽ chứa các file JSON kết quả cho từng ảnh và một file `summary.json` tổng kết.
    - Thư mục chứa ảnh (`IMAGE_FOLDER`) có thể chứa các định dạng ảnh phổ biến như .png, .jpg, .jpeg, .gif, .bmp.
    - Chạy script với tốc độ song song cho nhiều ảnh cùng lúc để tiết kiệm thời gian xử lý.
"""


import json
import requests
import base64
import os
from concurrent.futures import ThreadPoolExecutor
import time

# Thông tin config từ file JSON
with open('api/kdk.json', 'r') as f:
    config = json.load(f)

# Đường dẫn đến thư mục chứa ảnh
IMAGE_FOLDER = "MidTerm/test_data"  # Thay đổi thành thư mục chứa ảnh của bạn
# Đường dẫn để lưu kết quả
RESULT_FOLDER = "result"  # Thư mục lưu kết quả

# Tạo thư mục results nếu chưa tồn tại
if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)

def process_image(image_path):
    try:
        # Đọc và mã hóa ảnh
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Tạo payload với config từ file JSON và ảnh đã mã hóa
        payload = config.copy()
        payload["image"] = encoded_image

        # Gửi request
        response = requests.post(
            "https://ocr.kandianguji.com/ocr_api",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Lấy tên file từ đường dẫn
        image_name = os.path.basename(image_path)
        
        # Lưu kết quả
        result = {
            "image_name": image_name,
            "status_code": response.status_code,
            "response": response.json()
        }
        
        # Lưu kết quả vào file riêng
        result_file = os.path.join(RESULT_FOLDER, f"{image_name}_result.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
            
        print(f"Processed: {image_name}")
        return result
        
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return {"image_name": os.path.basename(image_path), "error": str(e)}

def main():
    # Lấy danh sách các file ảnh
    image_files = [
        os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
    ]
    
    start_time = time.time()
    results = []
    
    # Xử lý song song với ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_image, image_files))
    
    # Lưu tổng kết
    summary = {
        "total_images": len(image_files),
        "successful": len([r for r in results if 'error' not in r]),
        "failed": len([r for r in results if 'error' in r]),
        "processing_time": time.time() - start_time,
        "results": results
    }
    
    # Lưu summary vào file
    with open(os.path.join(RESULT_FOLDER, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
    
    print(f"\nProcessing completed!")
    print(f"Total images: {summary['total_images']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Total time: {summary['processing_time']:.2f} seconds")

if __name__ == "__main__":
    main()