import os
import re

def clean_text_file(file_path):
    # Đọc nội dung file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Tách nội dung thành các dòng
    lines = content.split('\n')
    
    # Tìm tất cả các dòng in hoa (có thể là tiêu đề)
    uppercase_lines = [line.strip() for line in lines if line.strip().isupper()]
    
    # Nếu có nhiều hơn một tiêu đề, giữ phần từ đoạn tiêu đề cuối cùng trở đi
    if len(uppercase_lines) > 1:
        # Tìm vị trí của dòng tiêu đề cuối cùng
        last_uppercase_line = uppercase_lines[-1]
        last_uppercase_line_index = next(
            i for i, line in enumerate(lines) if line.strip() == last_uppercase_line
        )
        # Kiểm tra và giữ lại các dòng in hoa liên tiếp trước tiêu đề cuối cùng
        while last_uppercase_line_index > 0 and lines[last_uppercase_line_index - 1].strip().isupper():
            last_uppercase_line_index -= 1
        lines = lines[last_uppercase_line_index:]

    
    # Xác định tiêu đề và nội dung
    title_lines = []
    content_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.isupper():
            # Gộp dòng tiêu đề liên tiếp
            title_lines.append(stripped_line)
        else:
            # Phát hiện bắt đầu nội dung
            content_lines.append(line)
    
    # Gộp các dòng tiêu đề thành một dòng duy nhất
    title = ' '.join(title_lines)
    
    # Làm sạch nội dung phần thân
    cleaned_content_lines = []
    for line in content_lines:
        # Loại bỏ các số không nằm trong ngoặc
        cleaned_line = re.sub(r'(?<!\()\b\d+\b(?!\))', '', line)
        # Chỉ thêm dòng không rỗng
        if cleaned_line.strip():
            cleaned_content_lines.append(cleaned_line.strip())
    
    # Kết hợp tiêu đề và nội dung
    cleaned_content = f"{title}\n" + '\n'.join(cleaned_content_lines)
    return cleaned_content

def process_folder(input_folder, output_folder):
    # Tạo thư mục đầu ra nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)
    
    # Duyệt qua từng file trong thư mục đầu vào
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            try:
                # Làm sạch file txt
                cleaned_content = clean_text_file(input_path)
                
                # Ghi nội dung đã làm sạch vào file mới
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(cleaned_content)
                
                print(f"Processed: {filename}")
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Thư mục đầu vào và đầu ra
input_folder = 'MidTerm/src/add translation column/data'
output_folder = 'MidTerm/src/add translation column/cleant_data'

# Chạy xử lý
process_folder(input_folder, output_folder)
