import requests

# Đường dẫn API
url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/sinonom-prose-translation"  # Cập nhật URL chính xác

# Headers
headers = {
    "User-Agent": "PostmanRuntime/7.42.0",  # Đảm bảo User-Agent hợp lệ
    "Content-Type": "application/json"
}

# Dữ liệu cần gửi (văn bản chữ Hán cần dịch)
data = {
    "text": "賜進士第陪從右侍郎東河子" 
}

# Gửi POST request
response = requests.post(url, json=data, headers=headers)

# Kiểm tra phản hồi từ API
if response.status_code == 200:
    result = response.json()  # Parse kết quả JSON
    print("Phản hồi từ API:", result)  # In ra toàn bộ phản hồi để kiểm tra chi tiết

    if result.get("is_success"):
        # In kết quả dịch
        print("Kết quả dịch:", result["data"]["result"][0])
    else:
        # In chi tiết lỗi từ API nếu có
        print("Lỗi từ API:", result.get("message", "Không rõ lỗi"))
else:
    print("Lỗi HTTP:", response.status_code, response.text)
