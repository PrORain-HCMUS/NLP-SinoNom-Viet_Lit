import os
import pandas as pd
import requests
import time

def transliterate_sinonom(text):
    """Chuyển tự chữ Hán Nôm sang chữ Quốc ngữ"""
    url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/sinonom-transliteration"
    
    headers = {
        "User-Agent": "PostmanRuntime/7.42.0",
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("is_success"):
                return result["data"]["result_text_transcription"][0]
            else:
                print(f"API error for text {text}: {result.get('message', 'Unknown error')}")
                return ''
        else:
            print(f"HTTP error for text {text}: {response.status_code}")
            return ''
    
    except Exception as e:
        print(f"Exception occurred for text {text}: {e}")
        return ''

def update_excel_with_transliteration(input_excel_path, output_excel_path):
    # Đọc file Excel
    df = pd.read_excel(input_excel_path)
    
    # Tạo một danh sách để lưu các âm Hán Việt
    han_viet_trans = []
    
    # Duyệt qua từng dòng và gọi API
    for index, row in df.iterrows():
        sino_nom_char = row['SinoNom Char']
        
        # Gọi API để chuyển tự
        han_viet = transliterate_sinonom(sino_nom_char)
        han_viet_trans.append(han_viet)
        
        # Thêm độ trễ để tránh quá tải API
        time.sleep(0.5)
    
    # Thêm cột 'Âm Hán Việt' vào DataFrame
    df['Âm Hán Việt'] = han_viet_trans
    
    # Lưu file Excel mới
    df.to_excel(output_excel_path, index=False, engine='openpyxl')
    print(f"Updated Excel file created at {output_excel_path}")

# Đường dẫn file Excel đầu vào và đầu ra
input_excel_path = 'MidTerm/output_csv/sino_nom_ocr_results.xlsx'
output_excel_path = 'MidTerm/output_csv/api_sinonom.xlsx'

# Chạy hàm cập nhật Excel
update_excel_with_transliteration(input_excel_path, output_excel_path)