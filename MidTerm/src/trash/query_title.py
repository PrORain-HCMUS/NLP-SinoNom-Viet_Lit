'''
# Giả sử bạn có các thông tin sau cho mỗi trang  
pages = [  
    {  
        "id": "TTVH6_057",  
        "title": "扈駕征順紀行",  
        "sentences": [  
            {"text": "乘風志士喜功名", "bounding_box": [678, 2366, 1237, 2434]},   # Câu cuối  
        ]  
    },  
    {  
        "id": "TTVH6_058",  
        "title": "南溟自此鯨波帖",  
        "sentences": [  
            {"text": "南溟自此鯨波帖", "bounding_box": [714, 245, 1287, 314]},   # Câu đầu  
            {"text": "江漢湯湯佇告成", "bounding_box": [715, 346, 1285, 419]},   # Câu thứ hai  
        ]  
    }  
]  

# Đoạn mã để kiểm tra tiêu đề cho các trang liền kề  
for i in range(len(pages) - 1):  
    previous_page = pages[i]  
    next_page = pages[i + 1]  
    
    # Lấy câu cuối của trang trước  
    last_sentence_prev = previous_page["sentences"][-1]["text"]  
    len_last_sentence_prev = len(last_sentence_prev)  

    # Kiểm tra câu đầu của trang sau  
    first_sentence_next = next_page["sentences"][0]["text"]  
    len_first_sentence_next = len(first_sentence_next)  

    # Kiểm tra câu thứ hai của trang sau (nếu có)  
    len_second_sentence_next = len(next_page["sentences"][1]["text"]) if len(next_page["sentences"]) > 1 else 0  

    # Kiểm tra yếu tố 1: Câu đầu thuộc phần đầu trang  
    # (Giả sử tọa độ bounding box được lưu lưu trữ ở dạng mảng)  
    is_in_first_part = next_page["sentences"][0]["bounding_box"][1] < 300  # Chỉ ví dụ  

    # Kiểm tra yếu tố 2: So sánh độ dài ký tự  
    condition_1 = (len_last_sentence_prev == len_first_sentence_next)  
    condition_2 = (len_last_sentence_prev == len_second_sentence_next)  

    # Nếu thỏa mãn cả 2 điều kiện  
    if is_in_first_part and (condition_1 or condition_2):  
        next_page["title"] = previous_page["title"]  # Gán tiêu đề  

# Kết quả  
for page in pages:  
    print(f"ID: {page['id']}, Title: {page['title']}")
'''



import pandas as pd
import ast

def extract_titles_from_excel(file_path):
    # Đọc file Excel
    df = pd.read_excel(file_path)
    
    titles = []
    current_id = None
    title = None
    previous_title = None
    last_text = None
    previous_page = None

    # Duyệt qua từng dòng trong DataFrame
    for index, row in df.iterrows():
        row_id = row['ID']
        char = row['Âm Hán Việt']
        image_box = row['ImageBox']
        
        # Kiểm tra xem image_box có phải là kiểu dữ liệu hợp lệ không
        if isinstance(image_box, str):
            try:
                image_box = ast.literal_eval(image_box)  # Chuyển chuỗi về dạng list
            except:
                continue  # Nếu không thể chuyển đổi, bỏ qua dòng này
        
        # Nếu image_box không có tọa độ hợp lệ, bỏ qua dòng này
        if not image_box or len(image_box) < 1:
            continue
        
        # Lấy số trang từ ID (phần số sau dấu gạch dưới)
        try:
            page_number = int(row_id.split('_')[-1])  # Lấy số trang từ ID, ví dụ TTVH6_057 -> 57
        except ValueError:
            continue  # Nếu không thể chuyển đổi thành số, bỏ qua dòng này
        
        # Chuyển ID thành số để so sánh
        current_id_number = int(row_id.split('_')[-1])  # Tách phần số từ ID và chuyển thành int
        
        # Kiểm tra nếu ID và trang thay đổi
        if current_id_number != (int(current_id.split('_')[-1]) if current_id else None):
            if title:  # Lưu lại tiêu đề cũ nếu không phải trang đầu tiên
                titles.append((current_id, title))
            title = char.strip()  # Cập nhật tiêu đề mới
            current_id = row_id

        # Kiểm tra điều kiện nối văn bản giữa hai trang (chỉ xét các trang liên tiếp)
        if previous_page is not None and page_number == previous_page + 1:
            # Điều kiện nối văn bản chỉ xét khi 2 trang liên tiếp
            first_line_match = len(char.strip().split()) == len(last_text.strip().split())
            
            # Điều kiện 2: Đếm số lượng ký tự trong câu đầu trang sau và câu cuối trang trước
            second_line_match = False
            if index + 1 < len(df):
                next_row = df.iloc[index + 1]  # Lấy dòng tiếp theo
                next_char = next_row['Âm Hán Việt']
                
                # Nếu dòng tiếp theo cùng ID và ở trang sau
                if next_row['ID'] == row_id and len(next_char.strip()) == len(last_text.strip()):
                    second_line_match = True
            
            # Nếu thỏa mãn điều kiện 1 hoặc điều kiện 2 và là các trang liên tiếp
            if first_line_match or second_line_match:
                title = previous_title  # Gán tiêu đề của trang trước cho trang sau
        else:
            # Nếu không phải trang liên tiếp (x-2 trở đi), gán tiêu đề mới cho trang hiện tại
            if previous_page is not None and page_number > previous_page + 1:
                title = char.strip()
            else:
                # Nếu vẫn tiếp tục với trang liên tiếp, giữ tiêu đề của trang trước
                title = previous_title if previous_title else char.strip()

        # Lưu lại thông tin cho trang trước
        previous_page = page_number
        last_text = char.strip()
        previous_title = title

    # Lưu tiêu đề cuối cùng
    if title and title not in [t[1] for t in titles]:
        titles.append((current_id, title))

    return titles

# Đường dẫn đến file Excel của bạn
file_path = 'MidTerm/output_csv/TTVH6_LHVu.xlsx'

# Lấy danh sách tiêu đề
titles = extract_titles_from_excel(file_path)

# Ghi danh sách tiêu đề vào file
output_file_path = 'MidTerm/output_csv/titles.txt'

with open(output_file_path, 'w', encoding='utf-8') as file:
    for idx, title in enumerate(titles, 1):
        if len(title[1]) > 2:  # Lọc ra các tiêu đề hợp lệ
            file.write(f"{idx}. {title[1]}\n")

print(f"Đã ghi danh sách tiêu đề vào {output_file_path}")
