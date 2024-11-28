#fill_mask = pipeline("fill-mask", model="bert-base-chinese")
#corrected = fill_mask("霜横碧[MASK]虹初霽")
#print(corrected)

'''
[{'score': 0.3700135350227356, 'token': 8024, 'token_str': '，', 'sequence': '霜 横 碧 ， 虹 初 霽'}, 
{'score': 0.07445497810840607, 'token': 510, 'token_str': '、', 'sequence': '霜 横 碧 、 虹 初 霽'}, 
{'score': 0.03774739056825638, 'token': 7433, 'token_str': '雨', 'sequence': '霜 横 碧 雨 虹 初 霽'}, 
{'score': 0.02158243954181671, 'token': 4819, 'token_str': '碧', 'sequence': '霜 横 碧 碧 虹 初 霽'}, 
{'score': 0.02047676034271717, 'token': 3717, 'token_str': ' 水', 'sequence': '霜 横 碧 水 虹 初 霽'}]
'''

from underthesea import word_tokenize
from transformers import pipeline

# Khởi tạo mô hình BERT cho tiếng Việt
fill_mask = pipeline("fill-mask", model="vinai/phobert-base")

# Phân tách từ trong câu
def preprocess_sentence(sentence):
    return word_tokenize(sentence)

def check_inaccuracy(sentence):
    words = preprocess_sentence(sentence)  # Tách câu thành các từ
    errors = []  # Lưu từ có khả năng sai

    for i, word in enumerate(words):
        # Tạo câu với từ bị che, thay thế [MASK] bằng <mask>
        masked_sentence = " ".join(words[:i] + ["<mask>"] + words[i+1:])
        predictions = fill_mask(masked_sentence)

        # Dự đoán các từ và score (xác suất)
        for prediction in predictions:
            top_prediction = prediction['token_str']
            score = prediction['score']

            # Tránh các từ không xác định (UNknown)
            if top_prediction == '[UNK]':
                continue
            
            # Điều chỉnh ngưỡng dự đoán, tránh những từ không phù hợp
            if top_prediction != word and score > 0.3:  # Thử nâng ngưỡng để tránh kết quả ngẫu nhiên
                errors.append((word, top_prediction, score))  # Ghi lại từ gốc, từ dự đoán và score

    return errors

# Ví dụ câu
sentence = "sương hoành bích hoắc hồng sơ tễ"
errors = check_inaccuracy(sentence)

# Kết quả
print("Từ có khả năng sai và dự đoán:", errors)
