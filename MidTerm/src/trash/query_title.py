import pandas as pd
import ast
import unicodedata
import re

def extract_abbreviation(title):
    # Remove diacritical marks
    normalized = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('utf-8')
    
    # Split into words and take first letters
    words = normalized.split()
    
    # Special handling for Vietnamese words
    abbr = ''.join([word[0].upper() for word in words])
    
    return abbr

def extract_titles_from_excel(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)
    
    titles = {}
    current_id = None
    title = None
    previous_title = None
    last_text = None
    previous_page = None

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        row_id = row['ID']
        char = row['Âm Hán Việt']
        image_box = row['ImageBox']
        
        # Check if image_box is a valid data type
        if isinstance(image_box, str):
            try:
                image_box = ast.literal_eval(image_box)  # Convert string to list
            except:
                continue  # Skip this row if conversion fails
        
        # Skip if no valid image box coordinates
        if not image_box or len(image_box) < 1:
            continue
        
        # Get page number from ID
        try:
            page_number = int(row_id.split('_')[-1])
        except ValueError:
            continue  # Skip if cannot convert to number
        
        # Convert ID to number for comparison
        current_id_number = int(row_id.split('_')[-1])
        
        # Check if ID and page change
        if current_id_number != (int(current_id.split('_')[-1]) if current_id else None):
            if title:  # Save previous title if not first page
                if title not in titles:
                    titles[title] = 1
                else:
                    titles[title] += 1
            title = char.strip()  # Update new title
            current_id = row_id

        # Check text connection conditions between two pages
        if previous_page is not None and page_number == previous_page + 1:
            # First condition: equal number of words
            first_line_match = len(char.strip().split()) == len(last_text.strip().split())
            
            # Second condition: equal character length
            second_line_match = False
            if index + 1 < len(df):
                next_row = df.iloc[index + 1]
                next_char = next_row['Âm Hán Việt']
                
                # If next row is same ID and page, check character length
                if next_row['ID'] == row_id and len(next_char.strip()) == len(last_text.strip()):
                    second_line_match = True
            
            # If conditions met and pages are consecutive
            if first_line_match or second_line_match:
                title = previous_title  # Use previous page's title
        else:
            # If not consecutive pages
            if previous_page is not None and page_number > previous_page + 1:
                title = char.strip()
            else:
                # Continue with previous page's title
                title = previous_title if previous_title else char.strip()

        # Save information for previous page
        previous_page = page_number
        last_text = char.strip()
        previous_title = title

    # Save last title
    if title:
        if title not in titles:
            titles[title] = 1
        else:
            titles[title] += 1

    return titles

# Path to Excel file
file_path = 'MidTerm/output_csv/TTVH6_LHVu.xlsx'

# Get titles with line counts
titles_dict = extract_titles_from_excel(file_path)

# Write titles to file with abbreviations and line counts
output_file_path = 'MidTerm/output_csv/titles_with_count.txt'

with open(output_file_path, 'w', encoding='utf-8') as file:
    for idx, (title, count) in enumerate(titles_dict.items(), 1):
        if len(title) > 2:  # Filter valid titles
            abbr = extract_abbreviation(title)
            file.write(f"{idx}. {title}, {abbr}, {count}\n")

print(f"Titles with counts written to {output_file_path}")