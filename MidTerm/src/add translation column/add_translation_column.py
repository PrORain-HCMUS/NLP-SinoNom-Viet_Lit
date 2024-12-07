"""
File Name: add_translation_column.py
Author: Lê Hoàng Vũ
Date: 07.12.2024
Description:
    - Script này đọc dữ liệu từ file Excel, thêm một cột 'Dịch nghĩa' vào DataFrame.
    - Dữ liệu trong cột 'Dịch nghĩa' được lấy từ các file .txt, mỗi file tương ứng với một trang trong dữ liệu.
    - Các dòng dịch nghĩa từ file .txt sẽ được thêm vào cột 'Dịch nghĩa' của mỗi dòng trong DataFrame, theo thứ tự ID của mỗi nhóm.
    - Sau khi thêm cột 'Dịch nghĩa', file Excel mới sẽ được lưu lại.
Input:
    - File Excel đầu vào (excel_file_path): Chứa các cột 'ID' và các thông tin văn bản cần dịch.
    - Thư mục chứa file dịch nghĩa (txt_dir_path): Các file .txt chứa các dòng dịch nghĩa tương ứng với mỗi trang.
    - File Excel đầu ra (output_file_path): File Excel mới sau khi đã thêm cột 'Dịch nghĩa'.
Output:
    - File Excel đầu ra (output_file_path): Bao gồm cột 'Dịch nghĩa' đã được cập nhật từ các file dịch nghĩa.
Usage:
    - Định nghĩa đường dẫn file Excel đầu vào, thư mục chứa file dịch nghĩa và đường dẫn file đầu ra.
    - Chạy script:
        python add_translation_column.py
Notes:
    - Đảm bảo rằng các file dịch nghĩa có tên theo định dạng "page_001.txt", "page_002.txt", ...
    - Số dòng trong file dịch nghĩa sẽ được cắt bớt nếu nhiều hơn số dòng trong mỗi trang của file Excel.
    - Hàm `get_translation_from_file` đọc tất cả các dòng từ file .txt và loại bỏ ký tự thừa.
    - Các file dịch nghĩa phải được lưu trữ trong thư mục chính xác.
    - Nếu file dịch nghĩa không tồn tại, dòng tương ứng sẽ không được cập nhật.
"""



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
txt_dir_path = 'MidTerm/src/add translation column/clean_data'  # Đảm bảo đường dẫn đúng
output_file_path = 'MidTerm/output_csv/TTVH6_full.xlsx'

# Gọi hàm để thêm cột Dịch nghĩa và lưu file Excel mới
add_translation_column(excel_file_path, txt_dir_path, output_file_path)