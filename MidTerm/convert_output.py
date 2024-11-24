import pandas as pd
import json
from collections import defaultdict
from xlsxwriter.workbook import Workbook
import unicodedata

def read_vietnamese_text(filename):
    """Read Vietnamese text file and return list of non-empty lines"""
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def read_data(filename):
    """Read Label.txt file"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()

def clean_text(text):
    """Clean text by removing punctuation and extra spaces"""
    if pd.isna(text):
        return ""
    text = str(text).strip().lower()
    return text

def convert_to_int(point_list):
    """Convert string coordinates to integers"""
    return [[int(x) for x in point] for point in point_list]

def pair_and_sort_boxes(boxes):
    """Sort and pair text boxes based on their position"""
    sorted_boxes = sorted(boxes, key=lambda box: -max(point[0] for point in box['points']))
    pairs = []
    current_pair = []
    max_x = float('-inf')
    
    for box in sorted_boxes:
        current_x = max(point[0] for point in box['points'])
        
        if len(current_pair) == 0:
            current_pair.append(box)
            max_x = current_x
        elif abs(current_x - max_x) <= 40:
            current_pair.append(box)
            current_pair.sort(key=lambda b: min(point[1] for point in b['points']))
            pairs.extend(current_pair)
            current_pair = []
            max_x = float('-inf')
        else:
            if current_pair:
                pairs.extend(current_pair)
            current_pair = [box]
            max_x = current_x
    
    if current_pair:
        pairs.extend(current_pair)
    
    return pairs

class TextAnalyzer:
    def __init__(self):
        self.sinonom_similar_dict = {}
        self.quocngu_sinonom_dict = {}
        
    def load_dictionaries(self):
        """Load and initialize dictionaries"""
        try:
            # Đọc file Excel với từ điển tương đồng
            sinonom_similar_df = pd.read_excel('SinoNom_similar_Dic.xlsx')
            # Đọc file Excel với từ điển Quốc ngữ - Hán Nôm
            qn_sinonom_df = pd.read_excel('QuocNgu_SinoNom_Dic.xlsx')
            
            # Xử lý từ điển tương đồng
            for _, row in sinonom_similar_df.iterrows():
                input_char = str(row[sinonom_similar_df.columns[0]]).strip()
                if pd.isna(input_char) or not input_char:
                    continue
                    
                similar_chars_str = str(row[sinonom_similar_df.columns[1]])
                similar_chars = {c.strip() for c in similar_chars_str.split(',') if c.strip()}
                similar_chars.add(input_char)
                self.sinonom_similar_dict[input_char] = similar_chars
                
            # Xử lý từ điển Quốc ngữ - Hán Nôm
            for _, row in qn_sinonom_df.iterrows():
                quoc_ngu = str(row['QuocNgu']).strip().lower() if 'QuocNgu' in qn_sinonom_df.columns else str(row[0]).strip().lower()
                han_nom = str(row['SinoNom']).strip() if 'SinoNom' in qn_sinonom_df.columns else str(row[1]).strip()
                
                if pd.isna(quoc_ngu) or pd.isna(han_nom) or not quoc_ngu or not han_nom:
                    continue
                
                for word in quoc_ngu.split():
                    if word not in self.quocngu_sinonom_dict:
                        self.quocngu_sinonom_dict[word] = set()
                    self.quocngu_sinonom_dict[word].add(han_nom)
            
        except Exception as e:
            print(f"Error loading dictionaries: {str(e)}")
            raise
            
    def analyze_character(self, ocr_char, quoc_ngu_word):
        """
        Phân tích một ký tự OCR với một từ Quốc ngữ và trả về trạng thái màu sắc
        """
        # Lấy các ký tự tương tự từ OCR
        similar_chars = self.get_similar_chars(ocr_char)
        
        # Lấy các bản dịch có thể từ từ Quốc ngữ 
        possible_translations = self.get_possible_translations(quoc_ngu_word)
        
        # Tìm phần giao của hai tập hợp
        intersection = similar_chars.intersection(possible_translations)
        
        # In thông tin debug nếu cần
        if self.debug_mode:
            print(f"\nPhân tích ký tự '{ocr_char}' với từ '{quoc_ngu_word}':")
            print(f"Tập S1 (các chữ tương đồng): {similar_chars}")
            print(f"Tập S2 (các bản dịch có thể): {possible_translations}")
            print(f"Giao của S1 và S2: {intersection}")

        # Quy tắc tô màu mới:
        if ocr_char in possible_translations:
            print("Kết quả: normal (ký tự OCR có trong các bản dịch có thể)")
            return 'normal'
        elif len(intersection) == 1:
            print("Kết quả: blue (1 ký tự chung)")
            return 'blue'
        elif len(intersection) > 1:
            print("Kết quả: red (nhiều ký tự chung)")
            return 'red'
        else:
            print("Kết quả: red (không có ký tự chung)")
            return 'red'

def process_and_save(raw_data, vietnamese_text_file, output_file):
    """Process the data and save to Excel"""
    analyzer = TextAnalyzer()
    analyzer.load_dictionaries()
    
    viet_lines = read_vietnamese_text(vietnamese_text_file)
    line_index = 0
    
    workbook = Workbook(output_file)
    worksheet = workbook.add_worksheet()

    # Define formats
    formats = {
        'default': workbook.add_format({'font_name': 'Nom Na Tong'}),
        'blue': workbook.add_format({'color': '#0000FF', 'font_name': 'Nom Na Tong'}),
        'red': workbook.add_format({'color': '#FF0000', 'font_name': 'Nom Na Tong'}),
        'header': workbook.add_format({'font_name': 'Nom Na Tong', 'bold': True})
    }

    # Write headers
    headers = ['ID', 'Image Box', 'SinoNom OCR', 'Chữ Quốc ngữ']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, formats['header'])

    row = 1
    for line in raw_data:
        filepath, data_part = line.split('\t')
        file_number = filepath.split('/')[-1].split('_')[1]
        parsed_data = json.loads(data_part)
        
        sorted_data = pair_and_sort_boxes(parsed_data)
        
        for item_idx, item in enumerate(sorted_data):
            quoc_ngu_text = viet_lines[line_index] if line_index < len(viet_lines) else ''
            if quoc_ngu_text:
                line_index += 1
            
            ocr_text = item['transcription']
            
            # Write data to Excel
            formatted_id = f"LCPv.{file_number}.001.{(item_idx+1):02d}"
            worksheet.write(row, 0, formatted_id, formats['default'])
            worksheet.write(row, 1, str(convert_to_int(item['points'])), formats['default'])
            
            # Process OCR text with color coding
            ocr_formats = []
            for char in ocr_text:
                status = analyzer.analyze_character(char, quoc_ngu_text)
                format_key = 'default' if status == 'normal' else status
                ocr_formats.extend([formats[format_key], char])
            
            if ocr_formats:
                worksheet.write_rich_string(row, 2, *ocr_formats)
            
            # Write Vietnamese text
            worksheet.write(row, 3, quoc_ngu_text, formats['default'])
            
            row += 1

    # Adjust column widths
    for col in range(len(headers)):
        worksheet.set_column(col, col, 20)

    workbook.close()
    print(f"Data has been saved to {output_file}")

def main():
    input_file = 'Label_kieu.txt'
    vietnamese_text_file = 'Kieu1866page045_vietnamese.txt'
    output_file = 'output_kieu.xlsx'
    
    try:
        raw_data = read_data(input_file)
        process_and_save(raw_data, vietnamese_text_file, output_file)
        print("Processing completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()