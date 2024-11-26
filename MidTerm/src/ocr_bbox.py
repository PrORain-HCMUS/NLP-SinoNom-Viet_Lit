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

def detect_text(path):
    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    # Lưu tọa độ bounding box của từng ký tự
    bounding_boxes = []
    current_line_boxes = []
    current_line_text = []
    last_bottom = None

    for text in texts[1:]:  # Bỏ qua phần tử đầu tiên (toàn bộ văn bản)
        vertices = text.bounding_poly.vertices
        char_box = [
            [vertices[0].x, vertices[0].y],  # Góc trái trên
            [vertices[1].x, vertices[1].y],  # Góc phải trên
            [vertices[2].x, vertices[2].y],  # Góc phải dưới
            [vertices[3].x, vertices[3].y]   # Góc trái dưới
        ]

        # Lọc văn bản Trung Quốc
        chinese_text = filter_chinese_text(text.description)
        
        if chinese_text:
            # Nếu có khoảng cách lớn giữa các dòng, kết thúc dòng hiện tại
            y1 = vertices[0].y
            y2 = vertices[2].y

            if last_bottom and y1 - last_bottom > 10 and current_line_boxes:
                # Tính bounding box cho toàn bộ dòng
                line_box = [
                    [min(box[0][0] for box in current_line_boxes), min(box[0][1] for box in current_line_boxes)],  # Trái trên
                    [max(box[1][0] for box in current_line_boxes), min(box[1][1] for box in current_line_boxes)],  # Phải trên
                    [max(box[2][0] for box in current_line_boxes), max(box[2][1] for box in current_line_boxes)],  # Phải dưới
                    [min(box[3][0] for box in current_line_boxes), max(box[3][1] for box in current_line_boxes)]   # Trái dưới
                ]
                
                bounding_boxes.append({
                    'text': ''.join(current_line_text),
                    'box': line_box
                })
                
                current_line_boxes = []
                current_line_text = []

            # Thêm văn bản và bounding box vào dòng hiện tại
            current_line_text.append(chinese_text)
            current_line_boxes.append(char_box)

            last_bottom = y2

    # Xử lý dòng cuối cùng
    if current_line_boxes:
        line_box = [
            [min(box[0][0] for box in current_line_boxes), min(box[0][1] for box in current_line_boxes)],  # Trái trên
            [max(box[1][0] for box in current_line_boxes), min(box[1][1] for box in current_line_boxes)],  # Phải trên
            [max(box[2][0] for box in current_line_boxes), max(box[2][1] for box in current_line_boxes)],  # Phải dưới
            [min(box[3][0] for box in current_line_boxes), max(box[3][1] for box in current_line_boxes)]   # Trái dưới
        ]
        
        bounding_boxes.append({
            'text': ''.join(current_line_text),
            'box': line_box
        })

    return texts, bounding_boxes

def ocr_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing {filename}...")

            # Nhận diện văn bản và lấy tọa độ bounding box
            texts, bounding_boxes = detect_text(file_path)

            # Tạo tên tệp txt tương ứng
            output_txt_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")

            with open(output_txt_path, "w", encoding="utf-8") as output_file:
                for line_data in bounding_boxes:
                    output_file.write(f"{line_data['text']} {line_data['box']}\n")
            
            # Kiểm tra xem tệp văn bản có rỗng không
            if os.path.getsize(output_txt_path) == 0:
                os.remove(output_txt_path)
                print(f"Removed empty file: {output_txt_path}")
            else:
                print(f"Results saved to {output_txt_path}")

# Đường dẫn thư mục đầu vào và đầu ra
input_folder = "MidTerm/test_data"  # Thư mục chứa ảnh
output_folder = "MidTerm/test_output"    # Thư mục lưu kết quả

# Gọi hàm để xử lý các ảnh trong thư mục đầu vào và lưu kết quả vào thư mục output
ocr_images_in_folder(input_folder, output_folder)