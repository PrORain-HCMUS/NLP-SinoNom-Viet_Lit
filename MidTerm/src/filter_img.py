import os
import shutil

# Thư mục chứa các file ảnh
data_folder = "MidTerm/data"
# Thư mục chứa các file tên
output_folder = "MidTerm/output"
# Thư mục để lưu ảnh đã được lọc
filtered_data_folder = "MidTerm/filtered_data"

# Tạo thư mục filtered_data nếu chưa tồn tại
if not os.path.exists(filtered_data_folder):
    os.makedirs(filtered_data_folder)

# Lấy danh sách các file tên trong thư mục output
output_files = [f for f in os.listdir(output_folder) if f.endswith(".txt")]

for filename in os.listdir(data_folder):
    if filename.endswith(".png"):
        # Trích xuất số thứ tự từ tên file
        index = int(filename.split("_")[1].split(".")[0])
        
        # Tạo tên file tên tương ứng
        output_filename = f"page_{index:03d}.txt"
        
        # Kiểm tra xem file tên có tồn tại trong thư mục output không
        if output_filename in output_files:
            # Copy file ảnh vào thư mục filtered_data
            src_path = os.path.join(data_folder, filename)
            dst_path = os.path.join(filtered_data_folder, filename)
            shutil.copy(src_path, dst_path)
            print(f"Copied {filename} to {filtered_data_folder}")