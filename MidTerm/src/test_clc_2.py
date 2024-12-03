import os, requests, json

url_upload = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"
url_ocr = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"

FOLDER_PATH = "./images/chi"
OUTPUT_PATH = "./output_chi"
OUTPUT_FILENAME = "filenames.json"


def load_or_initialize_output(output: str):
    """Tải file JSON hoặc khởi tạo dictionary rỗng nếu file không tồn tại hoặc bị rỗng."""
    if os.path.exists(output):
        if os.path.getsize(output) > 0:
            with open(output, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"File {output} bị rỗng, khởi tạo dictionary mới.")
    return {}

def save_to_output(output: str, data: dict):
    with open(output, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def detect_text(filepath: str):
    files = {
        'image_file': ('image.png', open(filepath, 'rb'), 'image/png')
    }

    response_upload = requests.post(url=url_upload, files=files, headers={"User-Agent": "test 123"})

    if response_upload.status_code == 200 and response_upload.json().get("is_success"):
        filename = response_upload.json().get("data", {}).get("file_name")

        if filename:
            data = load_or_initialize_output(OUTPUT_FILENAME)
            data[os.path.basename(filepath)] = filename
            save_to_output(OUTPUT_FILENAME, data)

            ocr_payload = {
                "ocr_id": 1,
                "file_name": filename
            }

            response_ocr = requests.post(
                url=url_ocr,
                json=ocr_payload,
                headers={"User-Agent": "test 123", "Content-Type": "application/json"}
            )

            if response_ocr.status_code == 200 and response_ocr.json().get("is_success"):
                result_bbox = response_ocr.json().get("data", {}).get("result_bbox", [])
                
                os.makedirs(OUTPUT_PATH, exist_ok=True)
                output_file = os.path.join(OUTPUT_PATH, os.path.basename(filepath).replace('.png', '.json'))

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result_bbox, f, ensure_ascii=False, indent=4)
                print(f"OCR kết quả đã được lưu tại: {output_file}")
            else:
                print(f"Lỗi OCR: {response_ocr.status_code} - {response_ocr.text}")
        else:
            print("Không tìm thấy filename từ API.")
    else:
        print(f"Lỗi khi upload file: {filepath}, mã lỗi {response_upload.status_code}.")

def main():
    for filename in os.listdir(FOLDER_PATH):
        filepath = os.path.join(FOLDER_PATH, filename)
        if os.path.isfile(filepath):
            detect_text(filepath)

if __name__ == "_main_":
    main()