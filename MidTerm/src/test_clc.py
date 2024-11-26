import requests

# Đường dẫn API
url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/sinonom-transliteration"

# Headers
headers = {
    "User-Agent": "PostmanRuntime/7.42.0",  # Đảm bảo User-Agent hợp lệ
    "Content-Type": "application/json"
}

# Dữ liệu cần gửi (văn bản chữ Hán cần chuyển tự)
data = {
    "text": "青山懷景"  # Nội dung chữ Hán mẫu
}

# Gửi POST request
response = requests.post(url, json=data, headers=headers)

# Kiểm tra phản hồi từ API
if response.status_code == 200:
    result = response.json()  # Parse kết quả JSON
    if result.get("is_success"):
        print("Chuyển tự:", result["data"]["result_text_transcription"][0])
    else:
        print("Lỗi từ API:", result.get("message", "Không rõ lỗi"))
else:
    print("Lỗi HTTP:", response.status_code, response.text)
