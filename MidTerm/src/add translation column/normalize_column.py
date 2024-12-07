import pandas as pd

def convert_ID_To_png(ID: str):
    """Chuyển ID thành tên file ảnh .png theo định dạng 'page_XXX.png'"""
    result = ID.split('_')[1]  
    result = result.zfill(3)  
    return f"TTVHVN6_page{result}.png"

def standardize_columns(file_path):
    # Đọc file Excel
    df = pd.read_excel(file_path)

    # Tạo cột 'Image_name' bằng cách chuyển đổi ID
    df['Image_name'] = df['ID'].apply(convert_ID_To_png)

    # Đổi tên cột 'SinoNom Char' thành 'SinoNom OCR'
    df = df.rename(columns={'SinoNom Char': 'SinoNom OCR'})

    # Chèn cột 'Image_name' ngay sau cột 'ID'
    cols = df.columns.tolist()  # Lấy danh sách tên cột
    cols.insert(cols.index('ID') + 1, cols.pop(cols.index('Image_name')))  # Di chuyển cột 'Image_name' ngay sau 'ID'
    df = df[cols]  # Sắp xếp lại thứ tự cột

    # Kiểm tra lại cấu trúc dữ liệu sau khi thay đổi
    print("Cấu trúc dữ liệu sau khi chuẩn hóa:")
    print(df.head())

    # Lưu lại file Excel đã chuẩn hóa
    output_path = file_path.replace('.xlsx', '_normalized.xlsx')
    df.to_excel(output_path, index=False)

    print(f"File đã được chuẩn hóa và lưu tại: {output_path}")

# Đọc và chuẩn hóa file Excel
input_file_path = 'MidTerm/output_csv/TTVH6_full.xlsx' 
standardize_columns(input_file_path)
