"""
File Name: convert_excel.py
Author: Lê Hoàng Vũ
Date: 25.11.2024
Description:
    - Script này chuyển các tệp văn bản (.txt) trong thư mục đầu vào thành một tệp Excel (.xlsx).
    - Mỗi tệp văn bản được đọc và các thông tin sau được trích xuất: ID từ tên tệp, văn bản SinoNom, và tọa độ bounding box của hình ảnh.
    - Tạo cột 'Âm Hán Việt' để thêm vào sau này (hiện tại để trống).
Features:
    1. Quét thư mục đầu vào và tìm các tệp văn bản (.txt).
    2. Đọc từng tệp văn bản và trích xuất thông tin từ mỗi dòng.
    3. Tạo tệp Excel với các cột: ID, ImageBox, SinoNom Char, và Âm Hán Việt.
    4. Lưu tệp Excel tại đường dẫn chỉ định.
Input:
    - Thư mục đầu vào (input_folder): Chứa các tệp văn bản .txt.
Output:
    - Tệp Excel đầu ra (output_excel_path): Lưu các dữ liệu đã chuyển đổi vào tệp .xlsx.
Usage:
    - Đặt đường dẫn thư mục đầu vào vào biến `input_folder` và đường dẫn tệp Excel đầu ra vào biến `output_excel_path`.
    - Chạy script:
        python convert_excel.py
Notes:
    - Tệp văn bản phải có định dạng: văn bản + bounding box với mỗi dòng chứa dữ liệu.
    - Cột 'Âm Hán Việt' sẽ được thêm vào sau trong các bước tiếp theo.
"""

import os
import pandas as pd

def convert_txt_to_excel(input_folder, output_excel_path):
    # List to store data from all text files
    all_data = []

    # Iterate through all text files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            # Extract ID from filename (remove .txt extension)
            file_id = os.path.splitext(filename)[0]
            
            # Full path to the text file
            file_path = os.path.join(input_folder, filename)
            
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Split the line into text and bounding box
                    parts = line.strip().split(' [[')
                    sino_nom_char = parts[0]
                    image_box = '[[' + parts[1]
                    
                    # Add to the data list
                    all_data.append({
                        'ID': file_id,
                        'ImageBox': image_box,
                        'SinoNom Char': sino_nom_char,
                        'Âm Hán Việt': ''  # Left blank as requested
                    })
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to Excel
    df.to_excel(output_excel_path, index=False, engine='openpyxl')
    print(f"Excel file created at {output_excel_path}")

# Specify input and output paths
input_folder = 'MidTerm/output'
output_excel_path = 'MidTerm/output_csv/TTVH6.xlsx'

# Run the conversion
convert_txt_to_excel(input_folder, output_excel_path)