"""
    Script nhỏ để test tính năng tool kandianguji ocr
"""

import json
import requests

# Đọc dữ liệu từ file JSON có sẵn
with open("KanDianKuJi.json", "r") as json_file:
    request_data = json.load(json_file)

# URL của API (bạn có thể chọn 1 trong 2 URL)
api_url = "https://ocr.kandianguji.com/ocr_api"
# Hoặc
# api_url = "https://images.kandianguji.com:14141/ocr_api"

# Headers cho request
headers = {
    "Content-Type": "application/json"
}

# Gửi POST request
try:
    response = requests.post(api_url, json=request_data, headers=headers)
    
    # Kiểm tra status code
    if response.status_code == 200:
        print("Success!")
        print("Response:", response.json())
    else:
        print("Error:", response.status_code)
        print("Response:", response.text)
        
except requests.exceptions.RequestException as e:
    print("Error occurred:", e)