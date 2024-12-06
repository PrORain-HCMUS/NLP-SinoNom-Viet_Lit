import pandas as pd
import os

# Hàm lấy nội dung dịch nghĩa từ file txt
def get_translation_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Đọc tất cả các dòng và loại bỏ ký tự thừa
        return [line.strip() for line in f.readlines()]

# Hàm để thêm cột Dịch nghĩa vào DataFrame
def add_translation_column(excel_file_path, txt_dir_path, output_file_path):
    # Đọc file Excel
    df = pd.read_excel(excel_file_path)
    
    # Tạo một cột mới 'Dịch nghĩa' và gán giá trị mặc định là NaN
    df['Dịch nghĩa'] = None
    
    # Lặp qua từng nhóm ID để xử lý
    grouped_df = df.groupby(df['ID'].str.split('_').str[1])
    
    for page_number, page_group in grouped_df:
        # Tìm file dịch nghĩa tương ứng với trang
        next_file = f"page_{int(page_number) + 1:03d}.txt"
        next_file_path = os.path.join(txt_dir_path, next_file)
        
        # Kiểm tra nếu file dịch nghĩa tồn tại
        if os.path.exists(next_file_path):
            translations = get_translation_from_file(next_file_path)
            
            # Nếu số lượng dòng dịch nhiều hơn số dòng văn bản, cắt bớt
            translations = translations[:len(page_group)]
            
            # Gán dịch nghĩa cho từng dòng trong nhóm
            for i, (_, row) in enumerate(page_group.iterrows()):
                if i < len(translations):
                    df.at[row.name, 'Dịch nghĩa'] = translations[i]

    # Lưu file Excel mới với cột Dịch nghĩa
    df.to_excel(output_file_path, index=False)
    print(f"File đã được lưu tại: {output_file_path}")

# Đường dẫn tới file Excel và thư mục chứa file dịch nghĩa
excel_file_path = 'MidTerm/output_csv/TTVH6_LHVu_updated.xlsx'
txt_dir_path = 'D:/Documents/HELP ME/MidTerm/src/add translation column/clean_data'  # Đảm bảo đường dẫn đúng
output_file_path = 'MidTerm/output_csv/TTVH6_full.xlsx'

# Gọi hàm để thêm cột Dịch nghĩa và lưu file Excel mới
add_translation_column(excel_file_path, txt_dir_path, output_file_path)