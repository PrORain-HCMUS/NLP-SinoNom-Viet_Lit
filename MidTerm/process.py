import json
import requests
import base64
import os
from concurrent.futures import ThreadPoolExecutor
import time

# Thông tin config từ file JSON
with open('kdk.json', 'r') as f:
    config = json.load(f)

# Đường dẫn đến thư mục chứa ảnh
IMAGE_FOLDER = "img"  # Thay đổi thành thư mục chứa ảnh của bạn
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