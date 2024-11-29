import os
import re

def process_text_file(file_path):
    """
    Process a text file with phonetic transcription and translation
    
    Args:
        file_path (str): Path to the input text file
    
    Returns:
        dict: Processed file contents
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n')
    
    result = {
        'phonetic_transcription': None,
        'phonetic_title': None,
        'translation': None,
        'translation_title': None
    }
    
    # Find phonetic transcription
    phonetic_index = -1
    for i, line in enumerate(content):
        if line.startswith('Phiên âm:'):
            phonetic_index = i
            # Find the first uppercase title or end of meaningful text
            transcription_end = next((j for j in range(i+1, len(content)) 
                                      if (content[j].isupper() and content[j] != '2') 
                                      or (content[j].strip() == '2') 
                                      or not content[j].strip()), 
                                     len(content))
            result['phonetic_transcription'] = '\n'.join(content[i+1:transcription_end]).strip()
            break
    
    # Find titles (all uppercase lines, excluding '2')
    titles = []
    for line in content:
        if line.isupper() and line.strip() != '2':
            titles.append(line)
    
    # Assign phonetic title
    if titles:
        result['phonetic_title'] = titles[0]
    
    return result

def process_folder(input_folder, output_folder):
    """
    Process all text files in input folder and write results to output folder
    
    Args:
        input_folder (str): Path to input text files
        output_folder (str): Path to save processed files
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each text file
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # Process the file
            result = process_text_file(input_path)
            
            # Write results to output file
            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.write(f"Phonetic Title: {result['phonetic_title'] or 'N/A'}\n\n")
                outfile.write(f"Phonetic Transcription:\n{result['phonetic_transcription'] or 'N/A'}\n\n")
                outfile.write(f"Translation Title: N/A\n\n")
                outfile.write(f"Translation:\nN/A")

# Main execution
if __name__ == "__main__":
    input_folder = 'MidTerm/src/add translation columns/test data'
    output_folder = 'MidTerm/src/add translation columns/test output'
    
    process_folder(input_folder, output_folder)
    print(f"Processed files from {input_folder} to {output_folder}")