"""
File Name: excel_normalize.py
Author: Lê Hoàng Vũ
Date: 27.11.2024
Description:
    - Script này đọc dữ liệu từ một file Excel, chỉnh sửa các giá trị trong một số cột, và lưu kết quả vào một file Excel mới.
    - Cột "ID" được chỉnh sửa để thay thế tiền tố "page_" bằng "TTVH6_".
    - Cột "Âm Hán Việt" được chỉnh sửa để viết hoa ký tự đầu tiên của mỗi giá trị.
    - Kết quả được lưu vào một file Excel mới với các thay đổi được áp dụng.
Features:
    1. Đọc dữ liệu từ một file Excel đầu vào.
    2. Thay đổi giá trị trong cột "ID" để thay thế "page_" thành "TTVH6_".
    3. Viết hoa ký tự đầu tiên trong cột "Âm Hán Việt".
    4. Lưu kết quả vào file Excel mới.
Input:
    - File Excel đầu vào (input_excel_path): Chứa dữ liệu cần chỉnh sửa.
Output:
    - File Excel đầu ra (output_excel_path): Chứa dữ liệu đã được chỉnh sửa.
Usage:
    - Đảm bảo rằng file Excel đầu vào có cấu trúc đúng và cột "ID" và "Âm Hán Việt" tồn tại.
    - Chạy script:
        python excel_normalize.py
Notes:
    - Cột "ID" sẽ có tiền tố "page_" thay bằng "TTVH6_".
    - Cột "Âm Hán Việt" sẽ được viết hoa chữ cái đầu tiên của mỗi giá trị.
    - Kết quả sẽ được lưu vào file Excel mới và không bao gồm chỉ mục của các dòng.
"""


import pandas as pd

# Đường dẫn file Excel đầu vào và đầu ra
input_excel_path = 'MidTerm/output_csv/LeHoangVu_TTVH6.xlsx'
output_excel_path = 'MidTerm/output_csv/TTVH6_LHVu.xlsx'

# Đọc file Excel đầu vào
df = pd.read_excel(input_excel_path)

# Chỉnh sửa cột ID
df['ID'] = df['ID'].str.replace('page_', 'TTVH6_', regex=False)

# Viết hoa ký tự đầu tiên trong cột Âm Hán Việt
df['Âm Hán Việt'] = df['Âm Hán Việt'].str.capitalize()

# Ghi kết quả ra file Excel đầu ra
df.to_excel(output_excel_path, index=False, engine='openpyxl')

print(f"Đã xử lý và lưu kết quả vào: {output_excel_path}")
