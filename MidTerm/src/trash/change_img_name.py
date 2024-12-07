import os
import shutil

folder_path = 'MidTerm/filtered_data'

for filename in os.listdir(folder_path):
    if filename.startswith('TTVHVN6_') and filename.endswith('.png'):
        old_path = os.path.join(folder_path, filename)
        new_filename = filename.replace('_page_', '_page')
        new_path = os.path.join(folder_path, new_filename)
        shutil.move(old_path, new_path)
        print(f"Đổi tên {filename} thành {new_filename}")