import os
from google.cloud import vision
from google.oauth2 import service_account

# Đường dẫn tới file key.json
key_path = "api/key.json"

# Thiết lập thông tin xác thực từ file key.json
credentials = service_account.Credentials.from_service_account_file(key_path)
client = vision.ImageAnnotatorClient(credentials=credentials)

# Hàm sử dụng Google Vision API để OCR ảnh
def detect_text_with_vision_api(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    
    if response.error.message:
        raise Exception(f"Google Vision API Error: {response.error.message}")
    
    texts = response.text_annotations
    if texts:
        # Trả về văn bản OCR đầy đủ (texts[0] là toàn bộ văn bản)
        return texts[0].description
    return ""

# Hàm xử lý folder ảnh và lưu kết quả OCR
def process_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Chỉ xử lý các file ảnh
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing {filename}...")

            try:
                # OCR ảnh
                ocr_text = detect_text_with_vision_api(file_path)

                # Tạo file txt tương ứng
                output_txt_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
                
                with open(output_txt_path, "w", encoding="utf-8") as output_file:
                    output_file.write(ocr_text)
                
                # Kiểm tra nội dung OCR
                if "Phiên âm" in ocr_text or "Dịch nghĩa" in ocr_text:
                    print(f"File {output_txt_path} contains 'Phiên âm' or 'Dịch nghĩa'. Keeping it.")
                else:
                    # Xóa file nếu không chứa từ khóa
                    os.remove(output_txt_path)
                    print(f"Removed file {output_txt_path} (no matching keywords).")
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Đường dẫn thư mục đầu vào và đầu ra
input_folder = "MidTerm/data"  # Thư mục chứa ảnh
output_folder = "MidTerm/src/add translation column/translation output"        # Thư mục lưu kết quả OCR

# Gọi hàm xử lý
process_images_in_folder(input_folder, output_folder)
