import os
from google.cloud import vision
from google.oauth2 import service_account

# Đường dẫn tới file key.json
key_path = "api/key.json"

# Thiết lập thông tin xác thực từ file key.json
credentials = service_account.Credentials.from_service_account_file(key_path)
client = vision.ImageAnnotatorClient(credentials=credentials)

# Hàm sử dụng Google Vision API để OCR ảnh và lấy thông tin bounding box
def detect_text_with_vision_api(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Vision API Error: {response.error.message}")

    annotations = []
    for text in response.text_annotations[1:]:  # Bỏ qua texts[0] (toàn bộ văn bản)
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        annotations.append({"text": text.description, "vertices": vertices})

    return annotations

# Hàm sắp xếp văn bản theo vị trí
def sort_annotations_by_position(annotations):
    # Sắp xếp dựa trên tọa độ y trước, sau đó đến x
    return sorted(annotations, key=lambda x: (x['vertices'][0][1], x['vertices'][0][0]))

# Hàm gộp văn bản theo dòng
def group_text_by_lines(annotations, line_threshold=10):
    lines = []
    current_line = []
    prev_y = None

    for annotation in annotations:
        y = annotation['vertices'][0][1]  # Tọa độ y của từ
        if prev_y is None or abs(y - prev_y) <= line_threshold:
            current_line.append(annotation['text'])
        else:
            lines.append(" ".join(current_line))
            current_line = [annotation['text']]
        prev_y = y

    if current_line:
        lines.append(" ".join(current_line))

    return lines

# Hàm xử lý thư mục ảnh và lưu kết quả OCR
def process_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Chỉ xử lý các file ảnh
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing {filename}...")

            try:
                # OCR ảnh và lấy thông tin bounding box
                annotations = detect_text_with_vision_api(file_path)
                sorted_annotations = sort_annotations_by_position(annotations)

                # Gộp văn bản theo dòng
                lines = group_text_by_lines(sorted_annotations)

                # Tạo file txt tương ứng
                output_txt_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")

                # Lưu kết quả văn bản OCR vào file
                with open(output_txt_path, "w", encoding="utf-8") as output_file:
                    output_file.write("\n".join(lines))

                # Kiểm tra nội dung OCR và chỉ giữ lại các file có chứa từ khóa "Dịch nghĩa"
                if "Dịch nghĩa" in "\n".join(lines):
                    print(f"File {output_txt_path} contains 'Dịch nghĩa'. Keeping it.")
                else:
                    # Xóa file nếu không chứa từ khóa "Dịch nghĩa"
                    os.remove(output_txt_path)
                    print(f"Removed file {output_txt_path} (no matching keyword 'Dịch nghĩa').")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Đường dẫn thư mục đầu vào và đầu ra
input_folder = "MidTerm/data"  # Thư mục chứa ảnh
output_folder = "MidTerm/src/add translation column/back up"  # Thư mục lưu kết quả OCR

# Gọi hàm xử lý
process_images_in_folder(input_folder, output_folder)
