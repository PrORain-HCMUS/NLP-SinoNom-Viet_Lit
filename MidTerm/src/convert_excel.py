import os
import pandas as pd

def convert_txt_to_excel(input_folder, output_excel_path):
    # List to store data from all text files
    all_data = []

    # Iterate through all text files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            # Extract ID from filename (remove .txt extension)
            file_id = os.path.splitext(filename)[0]
            
            # Full path to the text file
            file_path = os.path.join(input_folder, filename)
            
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Split the line into text and bounding box
                    parts = line.strip().split(' [[')
                    sino_nom_char = parts[0]
                    image_box = '[[' + parts[1]
                    
                    # Add to the data list
                    all_data.append({
                        'ID': file_id,
                        'ImageBox': image_box,
                        'SinoNom Char': sino_nom_char,
                        'Âm Hán Việt': ''  # Left blank as requested
                    })
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to Excel
    df.to_excel(output_excel_path, index=False, engine='openpyxl')
    print(f"Excel file created at {output_excel_path}")

# Specify input and output paths
input_folder = 'MidTerm/output'
output_excel_path = 'MidTerm/output_csv/TTVH6.xlsx'

# Run the conversion
convert_txt_to_excel(input_folder, output_excel_path)