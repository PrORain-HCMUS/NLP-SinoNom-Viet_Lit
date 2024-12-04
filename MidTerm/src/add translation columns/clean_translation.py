import os
import re

# Kiểm tra ký tự có phải ký tự Hán không
def is_chinese_character(char):
    return '\u4e00' <= char <= '\u9fff'

# Hàm lọc nội dung trong tệp .txt
def clean_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    cleaned_lines = []
    skip_block = False  # Biến kiểm tra có nên bỏ qua đoạn hiện tại không

    for line in lines:
        stripped_line = line.strip()

        # Kiểm tra ký tự Hán
        if any(is_chinese_character(char) for char in stripped_line):
            continue

        # Nếu dòng bắt đầu bằng số, kích hoạt bỏ qua đoạn văn
        if re.match(r"^\d+\.", stripped_line):  # Số + "." ở đầu dòng
            skip_block = True
            continue  # Bỏ qua dòng hiện tại

        # Nếu dòng rỗng, kết thúc đoạn hiện tại
        if not stripped_line:
            skip_block = False

        # Nếu đang trong đoạn cần bỏ qua, bỏ qua dòng
        if skip_block:
            continue

        # Xóa số ở cuối dòng nếu có
        cleaned_line = re.sub(r"\s+\d+$", "", stripped_line)  # Chỉ xóa số cuối, không làm ảnh hưởng nội dung khác

        # Chỉ thêm dòng nếu còn nội dung
        if cleaned_line.strip():
            cleaned_lines.append(cleaned_line)

    # Ghi nội dung đã lọc trở lại vào file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(cleaned_lines))
    print(f"File {file_path} đã được làm sạch.")

# Hàm duyệt qua tất cả các file .txt trong thư mục
def clean_all_txt_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(".txt"):
            print(f"Đang xử lý {filename}...")
            clean_text_file(file_path)


# Đường dẫn thư mục chứa các file .txt
output_folder = "MidTerm/src/add translation column/data"

# Gọi hàm xử lý
clean_all_txt_files_in_folder(output_folder)
