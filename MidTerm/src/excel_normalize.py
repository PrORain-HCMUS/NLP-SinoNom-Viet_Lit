import pandas as pd

# Đường dẫn file Excel đầu vào và đầu ra
input_excel_path = 'MidTerm/output_csv/LeHoangVu_TTVH6.xlsx'
output_excel_path = 'MidTerm/output_csv/TTVH6_LHVu.xlsx'

# Đọc file Excel đầu vào
df = pd.read_excel(input_excel_path)

# Chỉnh sửa cột ID
df['ID'] = df['ID'].str.replace('page_', 'TTVH6_', regex=False)

# Viết hoa ký tự đầu tiên trong cột Âm Hán Việt
df['Âm Hán Việt'] = df['Âm Hán Việt'].str.capitalize()

# Ghi kết quả ra file Excel đầu ra
df.to_excel(output_excel_path, index=False, engine='openpyxl')

print(f"Đã xử lý và lưu kết quả vào: {output_excel_path}")
