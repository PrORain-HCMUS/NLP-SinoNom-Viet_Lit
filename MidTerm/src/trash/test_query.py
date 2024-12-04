import pandas as pd  

# Dữ liệu ví dụ  
data = {  
    "ID": ["TTVH6_057"] * 8 + ["TTVH6_058"] * 2,  
    "ImageBox": [  
        [[671, 1548], [1256, 1549], [1255, 1637], [670, 1636]],  # Trang 1  
        [[804, 1685], [1117, 1686], [1116, 1760], [803, 1759]],  # Trang 2  
        [[682, 1861], [1242, 1861], [1242, 1926], [682, 1926]],  # Trang 3  
        [[681, 1960], [1241, 1960], [1241, 2026], [681, 2026]],  # Trang 4  
        [[688, 2061], [1252, 2061], [1252, 2132], [688, 2132]],  # Trang 5  
        [[678, 2163], [1237, 2163], [1237, 2230], [678, 2230]],  # Trang 6  
        [[676, 2261], [1238, 2260], [1239, 2330], [677, 2331]],  # Trang 7  
        [[678, 2366], [1237, 2366], [1237, 2434], [678, 2434]],  # Trang 8  
        [[714, 245], [1287, 245], [1287, 314], [714, 314]],      # Trang 9  
        [[715, 346], [1284, 344], [1285, 419], [716, 421]]       # Trang 10  
    ],  
    "SinoNom Char": [  
        "扈駕征順紀行", "珥河萑舟", "聖主方揚吊伐兵", "賒航先後豎神旌",  
        "臨流炫耀篷檣影", "壓浪喧闐鼓角聲", "扶日從臣慚算略", "乘風志士喜功名",  
        "南溟自此鯨波帖", "江漢湯湯佇告成"  
    ],  
    "Âm Hán Việt": [  
        "Hỗ giá chinh thuận kỷ hành", "Nhĩ hà hoàn chu", "Thánh chúa phương dương điếu phạt binh",  
        "Xa hàng tiên hậu thụ thần tinh", "Lâm lưu huyền diệu bồng tường ảnh",  
        "Áp lãng huyên điền cổ giốc thanh", "Phù nhật tòng thần tàm toan lược",  
        "Thừa phong chí sĩ hỉ công danh", "Nam minh tự thử kình ba thiếp",  
        "Giang hán thang thang giữ cáo thành"  
    ]  
}  

df = pd.DataFrame(data)  

# Gán tiêu đề theo điều kiện  
for i in range(len(df) - 1):  
    current_id = df.iloc[i]['ID']  
    next_id = df.iloc[i + 1]['ID']  
    
    # Kiểm tra nếu có 2 ID liên tiếp  
    if current_id == next_id:  
        continue  # Bỏ qua nếu cùng một ID  
        
    # Kiểm tra điều kiện tọa độ  
    next_bounding_box = df.iloc[i + 1]['ImageBox'][0]  # Câu đầu tiên của trang sau  
    first_bbox_y = next_bounding_box[1]  # Y tọa độ của câu đầu  

    if first_bbox_y > 300:  # Kiểm tra tọa độ Y  
        continue  

    # Câu cuối ở trang trước  
    last_sentence_current = df.iloc[i]['Âm Hán Việt']  # Câu cuối của trang trước  
    len_last_sentence = len(last_sentence_current)  

    # Câu đầu tiên và thứ hai của trang sau  
    first_sentence_next = df.iloc[i + 1]['Âm Hán Việt']  
    second_sentence_next = (df.iloc[i + 1]['Âm Hán Việt'] if (i + 2 < len(df) and df.iloc[i + 1]['ID'] == df.iloc[i + 2]['ID']) else None)  

    len_first_sentence_next = len(first_sentence_next)  
    len_second_sentence_next = len(second_sentence_next) if second_sentence_next else 0  

    # Điều kiện so sánh số ký tự  
    condition_1 = (len_last_sentence == len_first_sentence_next)  
    condition_2 = (len_last_sentence == len_second_sentence_next)  

    # Nếu thỏa mãn cả 2 điều kiện, gán tiêu đề  
    if condition_1 or condition_2:  
        df.at[i + 1, 'Âm Hán Việt'] = df.at[i, 'Âm Hán Việt']  

# Kết quả  
for index, row in df.iterrows():  
    print(f"ID: {row['ID']}, Title: {row['Âm Hán Việt']}")