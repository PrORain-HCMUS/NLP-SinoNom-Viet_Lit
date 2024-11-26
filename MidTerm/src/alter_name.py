import os

# Thư mục chứa các file
folder_path = "MidTerm/data"

for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        # Trích xuất số thứ tự từ tên file
        index = int(filename.split("_")[1].split(".")[0])
        
        # Tạo tên file mới
        new_filename = f"page_{index:03d}.png"
        
        # Đổi tên file
        old_filepath = os.path.join(folder_path, filename)
        new_filepath = os.path.join(folder_path, new_filename)
        os.rename(old_filepath, new_filepath)
        print(f"Renamed {filename} to {new_filename}")