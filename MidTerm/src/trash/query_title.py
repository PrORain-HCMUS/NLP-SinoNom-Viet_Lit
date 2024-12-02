import pandas as pd

# Đọc file Excel
def extract_titles_from_excel(file_path):
    # Đọc file Excel
    df = pd.read_excel(file_path)

    titles = []
    current_id = None
    title = None
    previous_title = None
    last_text = None
    last_bounding_box = None
    previous_page = None

    # Duyệt qua từng dòng trong DataFrame
    for index, row in df.iterrows():
        row_id = row['ID']
        char = row['Âm Hán Việt']
        image_box = row['ImageBox']
        
        # Kiểm tra xem image_box có phải là kiểu dữ liệu hợp lệ không
        if isinstance(image_box, str):
            try:
                image_box = eval(image_box)  # Chuyển chuỗi về dạng list nếu cần
            except:
                continue  # Nếu không thể chuyển đổi, bỏ qua dòng này
        
        # Nếu image_box không có tọa độ hợp lệ, bỏ qua dòng này
        if not image_box or len(image_box) < 1:
            continue
        
        # Lấy số trang từ ImageBox (hoặc có thể thêm logic để phân biệt trang)
        try:
            page_number = image_box[0][1]  # Cố gắng lấy số trang từ tọa độ
        except IndexError:
            continue  # Nếu không thể lấy số trang, bỏ qua dòng này
        
        # Kiểm tra xem ID và trang có thay đổi không
        if row_id != current_id:
            # Nếu tiêu đề có sự thay đổi, kiểm tra trang trước
            if title:
                titles.append((current_id, title))  # Lưu tiêu đề cũ
            title = char.strip()  # Cập nhật tiêu đề mới
            current_id = row_id

        # Kiểm tra các điều kiện để kết hợp tiêu đề giữa các trang
        if previous_page == page_number - 1:
            # Kiểm tra điều kiện: Câu đầu tiên của trang sau nằm ở phần đầu trang
            current_bounding_box = image_box
            if current_bounding_box[0][1] < 300:  # Xác định câu đầu có phải ở phần đầu trang
                # Kiểm tra câu cuối ở trang trước và câu đầu trang sau có cùng số ký tự
                if len(last_text) == len(char.strip()) or len(last_text) == len(char.strip()) - 1:
                    title = previous_title  # Giữ tiêu đề từ trang trước

        # Lưu lại thông tin của trang trước
        previous_page = page_number
        last_text = char.strip()
        last_bounding_box = image_box
        previous_title = title

    # Nếu có tiêu đề cuối cùng chưa được thêm vào danh sách
    if title and title not in [t[1] for t in titles]:
        titles.append((current_id, title))

    return titles

# Đường dẫn đến file Excel của bạn
file_path = 'MidTerm/output_csv/TTVH6_LHVu.xlsx'

# Lấy danh sách tiêu đề
titles = extract_titles_from_excel(file_path)

# Đường dẫn đến file txt cần ghi
output_file_path = 'MidTerm/output_csv/titles.txt'

# Ghi tiêu đề vào file txt
with open(output_file_path, 'w', encoding='utf-8') as file:
    for idx, title in enumerate(titles, 1):
        # Lọc ra các tên tiêu đề hợp lệ (loại bỏ những ký tự không phải tiêu đề)
        if len(title[1]) > 2:  # Kiểm tra tiêu đề có đủ dài hay không (hoặc bạn có thể thay đổi điều kiện này)
            file.write(f"{idx}. {title[1]}\n")

print(f"Đã ghi danh sách tiêu đề vào {output_file_path}")
