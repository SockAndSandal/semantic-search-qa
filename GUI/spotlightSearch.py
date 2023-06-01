import subprocess

def search_files_with_content(query, path):
    command = ['mdfind', '-interpret', query, '-onlyin', path]
    result = subprocess.run(command, capture_output=True, text=True)
    files = result.stdout.splitlines()
    return files

def extract_document_content(file_path):
    if file_path.endswith('.pdf'):
        command = ['pdftotext', file_path, '-']
    elif file_path.endswith('.docx'):
        command = ['docx2txt', file_path]
    elif file_path.endswith('.pages'):
        command = ['cat', file_path]
    else:
        return None
    
    result = subprocess.run(command, capture_output=True, text=True)
    document_content = result.stdout
    return document_content

# Example usage

if __name__ == "__main__":
    #model = QuestionAnswering(model_name="distilbert-base-cased-distilled-squad", revision="626af31")
    query = 'Ramkumar'  # Content you want to search for
    path = '/Users/ram/Desktop/Final-Project/Sample_Files'  # Specific path to search within
    #found_files = search_files_with_content(query, path)
    #print(found_files)
    # Example usage
    file_path = '/Users/ram/Desktop/Final-Project/Sample_Files/Direct_Answers_in_Google_Search_Results.pdf'  # Path to the file you want to extract content from
    content = extract_document_content(file_path)
    print(content)
