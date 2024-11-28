import pandas as pd
import requests
from transformers import pipeline

# Đọc dữ liệu từ tệp Excel
similar_df = pd.read_excel('dictionary/SinoNom_Similar_Dic_v2.xlsx')

# Chuyển đổi dữ liệu từ điển SinoNom_Similar_Dic_v2 thành dictionary
sino_similar_dict = similar_df.set_index('Input Character')['Top 20 Similar Characters'].apply(eval).to_dict()

# Khởi tạo mô hình BERT
fill_mask = pipeline("fill-mask", model="bert-base-chinese")

# Hàm dùng tool CLC để chuyển tự
def get_transliteration_from_api(text):
    url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/sinonom-transliteration"
    headers = {
        "User-Agent": "PostmanRuntime/7.42.0",  
        "Content-Type": "application/json"
    }
    data = {"text": text}  # Chữ Hán cần chuyển tự

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()  # Parse kết quả JSON
        if result.get("is_success"):
            return result["data"]["result_text_transcription"][0]
        else:
            print("Lỗi từ API:", result.get("message", "Không rõ lỗi"))
            return None
    else:
        print("Lỗi HTTP:", response.status_code, response.text)
        return None

# Hàm so sánh và chọn phiên âm đúng nhất
def compare_versions_with_mask(masked_sentence, candidates):
    """
    Dùng BERT để so sánh phiên âm các từ và chọn từ có score cao nhất.
    """
    best_match = None
    best_score = float('-inf')

    for candidate in candidates:
        candidate_sentence = masked_sentence.replace("[MASK]", candidate)
        predictions = fill_mask(candidate_sentence)

        # Đảm bảo rằng có thể có nhiều dự đoán từ BERT, chọn dự đoán đầu tiên
        if predictions:
            score = predictions[0]['score']  # Lấy điểm số của dự đoán

            # So sánh với score hiện tại để chọn từ có điểm số cao nhất
            if score > best_score:
                best_score = score
                best_match = candidate

    return best_match, best_score

# Kiểm tra phiên âm cho các ký tự tương tự
def check_similar_characters(han_character):
    similar_characters = list(sino_similar_dict.get(han_character, []))

    print(f"Ký tự Hán của '{han_character}': {han_character}")
    print(f"Các ký tự tương tự: {similar_characters}")

    # Lấy phiên âm cho mỗi ký tự tương tự
    transliterations = []
    for char in similar_characters:
        transliteration = get_transliteration_from_api(char)
        if transliteration:
            transliterations.append(transliteration)
            print(f"Phiên âm của '{char}': {transliteration}")

    return transliterations

# Đảm bảo rằng từ 'hoắc' đã được thay thế thành [MASK]
sentence = "sương hoành bích hoắc hồng sơ tễ"
masked_sentence = sentence.replace("hoắc", "[MASK]")

# Kiểm tra câu đã thay thế [MASK]
print("Câu đã thay thế [MASK]:", masked_sentence)

if "[MASK]" not in masked_sentence:
    print("Không tìm thấy token [MASK] trong câu!")
else:
    # Lấy ký tự Hán tương ứng với từ 'hoắc' và kiểm tra các ký tự tương tự
    han_character = "藿"
    transliterations = check_similar_characters(han_character)

    # So sánh các phiên âm đã thu được với câu có [MASK]
    best_match, best_score = compare_versions_with_mask(masked_sentence, transliterations)

    # In kết quả
    print(f"Phiên âm đúng nhất cho từ 'hoắc' là: {best_match} với điểm số {best_score}")
