import fitz  # PyMuPDF
import os
from pathlib import Path
import pdfplumber

def extract_pdf_content(pdf_path, text_output_dir, image_output_dir):
    """
    Trích xuất nội dung văn bản và hình ảnh từ PDF và lưu vào các thư mục riêng biệt.
    
    Args:
        pdf_path (str): Đường dẫn đến file PDF
        text_output_dir (str): Thư mục để lưu các file text 
        image_output_dir (str): Thư mục để lưu các file hình ảnh
    """
    # Tạo thư mục output nếu chưa tồn tại
    Path(text_output_dir).mkdir(parents=True, exist_ok=True)
    Path(image_output_dir).mkdir(parents=True, exist_ok=True)
    
    # Xử lý text bằng pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        for page_num in range(total_pages):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if text is not None and text.strip():
                text_filename = f"page_{str(page_num + 1).zfill(3)}.txt"
                text_path = os.path.join(text_output_dir, text_filename)
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Đã lưu text trang {page_num + 1}/{total_pages}: {text_filename}")
    
    # Xử lý hình ảnh bằng PyMuPDF
    pdf_document = fitz.open(pdf_path)
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        image_list = page.get_images()
        
        for img_num, img in enumerate(image_list):
            try:
                # Lấy thông tin hình ảnh
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_data = base_image["image"]
                
                # Xác định phần mở rộng file dựa vào định dạng hình ảnh
                image_ext = base_image["ext"]
                
                # Tạo tên file hình ảnh
                img_filename = f"page_{str(page_num + 1).zfill(3)}_image_{str(img_num + 1).zfill(3)}.{image_ext}"
                img_path = os.path.join(image_output_dir, img_filename)
                
                # Lưu hình ảnh
                with open(img_path, "wb") as f:
                    f.write(image_data)
                print(f"Đã lưu hình ảnh {img_num + 1} từ trang {page_num + 1}: {img_filename}")
            except Exception as e:
                print(f"Lỗi khi xử lý hình ảnh {img_num + 1} trang {page_num + 1}: {str(e)}")
    
    pdf_document.close()

def main():
    # Đường dẫn đến file PDF
    pdf_path = "Midterm/LeHoangTTVHVN6.pdf"
    text_output_dir = "extracted_text"
    image_output_dir = "Midterm/data"
    
    try:
        extract_pdf_content(pdf_path, text_output_dir, image_output_dir)
        print(f"\nHoàn thành!")
        print(f"Text đã được lưu trong thư mục: {text_output_dir}")
        print(f"Hình ảnh đã được lưu trong thư mục: {image_output_dir}")
    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    main()