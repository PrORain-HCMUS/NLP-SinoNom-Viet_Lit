"""
File Name: preprocessing.py
Author: Lê Hoàng Vũ
Date: 07.12.2024
Description:
    - Script này đọc dữ liệu từ file Excel, cập nhật cột 'ID' với chữ viết tắt 
      được tạo từ tiêu đề văn bản (cột 'Âm Hán Việt') trong dữ liệu.
    - Sau khi tạo chữ viết tắt từ tiêu đề, các ID trong file Excel sẽ được cập nhật với chữ viết tắt 
      và lưu vào một file Excel mới.
Input:
    - File Excel đầu vào (file_path): Chứa các cột 'ID', 'Âm Hán Việt' và 'ImageBox'.
    - Cột 'ID' chứa các giá trị ID dạng chuỗi, 'Âm Hán Việt' chứa các tiêu đề văn bản, 
      và 'ImageBox' chứa các tọa độ hình ảnh dưới dạng chuỗi.
Output:
    - File Excel đầu ra: Bao gồm cột 'ID' đã được cập nhật, trong đó mỗi ID sẽ có chữ viết tắt mới.
Usage:
    - Định nghĩa đường dẫn file Excel đầu vào và gọi hàm `update_id_with_abbreviations` để cập nhật ID.
    - Chạy script:
        python preprocessing.py
Notes:
    - Cần đảm bảo rằng cột 'ImageBox' chứa dữ liệu hợp lệ dưới dạng chuỗi tọa độ.
    - Các ID phải có định dạng đúng để có thể tách được số trang từ ID.
    - Hàm `extract_abbreviation` tạo chữ viết tắt từ tiêu đề, loại bỏ dấu diacritics và lấy chữ cái đầu của mỗi từ.
    - Nếu không thể chuyển đổi tọa độ trong 'ImageBox', dòng đó sẽ bị bỏ qua.
    - Hàm sẽ tự động bỏ qua các dòng nếu không có tọa độ hình ảnh hợp lệ hoặc nếu không thể tách được số trang từ ID.
"""



import pandas as pd
import ast
import unicodedata
import re
import os

def extract_abbreviation(title):
    # Remove diacritical marks
    normalized = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('utf-8')
    
    # Split into words and take first letters
    words = normalized.split()
    
    # Special handling for Vietnamese words
    abbr = ''.join([word[0].upper() for word in words if word])  # Avoid empty words
    
    return abbr

def update_id_with_abbreviations(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)
    
    titles = {}
    current_id = None
    title = None
    previous_title = None
    last_text = None
    previous_page = None

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        row_id = row['ID']
        char = row['Âm Hán Việt']
        image_box = row['ImageBox']
        
        # Check if image_box is a valid data type
        if isinstance(image_box, str):
            try:
                image_box = ast.literal_eval(image_box)  # Convert string to list
            except:
                continue  # Skip this row if conversion fails
        
        # Skip if no valid image box coordinates
        if not image_box or len(image_box) < 1:
            continue
        
        # Get page number from ID
        try:
            page_number = int(row_id.split('_')[-1])
        except ValueError:
            continue  # Skip if cannot convert to number
        
        # Convert ID to number for comparison
        current_id_number = int(row_id.split('_')[-1])
        
        # Check if ID and page change
        if current_id_number != (int(current_id.split('_')[-1]) if current_id else None):
            if title:  # Save previous title if not first page
                if title not in titles:
                    titles[title] = 1
                else:
                    titles[title] += 1
            title = char.strip()  # Update new title
            current_id = row_id

        # Check text connection conditions between two pages
        if previous_page is not None and page_number == previous_page + 1:
            # First condition: equal number of words
            first_line_match = len(char.strip().split()) == len(last_text.strip().split())
            
            # Second condition: equal character length
            second_line_match = False
            if index + 1 < len(df):
                next_row = df.iloc[index + 1]
                next_char = next_row['Âm Hán Việt']
                
                # If next row is same ID and page, check character length
                if next_row['ID'] == row_id and len(next_char.strip()) == len(last_text.strip()):
                    second_line_match = True
            
            # If conditions met and pages are consecutive
            if first_line_match or second_line_match:
                title = previous_title  # Use previous page's title
        else:
            # If not consecutive pages
            if previous_page is not None and page_number > previous_page + 1:
                title = char.strip()
            else:
                # Continue with previous page's title
                title = previous_title if previous_title else char.strip()

        # Save information for previous page
        previous_page = page_number
        last_text = char.strip()
        previous_title = title

        # Update ID with abbreviation in the DataFrame
        abbr = extract_abbreviation(title)
        df.at[index, 'ID'] = row_id + '_' + abbr  # Append abbreviation to ID

    # Save updated DataFrame to Excel
    updated_excel_path = file_path.replace('.xlsx', '_updated.xlsx')
    df.to_excel(updated_excel_path, index=False)
    
    return updated_excel_path

# Path to the Excel file
file_path = 'MidTerm/output_csv/TTVH6_LHVu.xlsx'

# Update the IDs in the Excel file
updated_excel_path = update_id_with_abbreviations(file_path)

print(f"File Excel đã được cập nhật và lưu tại: {updated_excel_path}")
