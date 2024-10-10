from collections import Counter
import time

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines

def extract_relevant_text(lines):
    start_idx = None
    end_idx = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith("*** START OF THIS PROJECT GUTENBERG EBOOK"):
            start_idx = i + 1
        if line.strip().startswith("*** END OF THIS PROJECT GUTENBERG EBOOK"):
            end_idx = i
            break
    
    if start_idx is None or end_idx is None:
        print("Error: Start or End markers not found in the file.")
        return ''
    
    return ''.join(lines[start_idx:end_idx])

def clean_text(text):
    new_text = text.replace("\n", "")
    new_text = text.replace(' ', "")
    lower_text = new_text.lower()
    clean_text = ""
    for char in lower_text:
        if char.isalnum() or char != " ":
            if char in "áéíóú":
                clean_text += "aeiou"["áéíóú".index(char)]
            elif char in "ñ":
                clean_text += "n"
            elif char in "äëïöü":
                clean_text += "aeiou"["äëïöü".index(char)]
            else:
                clean_text += char
    return clean_text

def count_characters(file_path, clean=False):
    start_time = time.time()
    
    lines = read_file(file_path)
    
    text = extract_relevant_text(lines)
    
    if clean:
        text = clean_text(text)
    
    char_count = Counter(text)
    
    sorted_char_count = []
    for char, count in char_count.items():
        sorted_char_count.append((char, count))
    
    sorted_char_count.sort(key=lambda item: item[1], reverse=True)
    
    total_time = time.time() - start_time
    
    return sorted_char_count, total_time

files = {
    "de": "de-10223-8_UTF8.txt",
    "en": "en-10012-8_UTF8.txt",
    "es": "es-11529-8_UTF8.txt",
    "fr": "fr-10682-8_UTF8.txt"
}

if __name__ == "__main__":

    for lang, file_path in files.items():
        print(file_path)
        result, exec_time = count_characters(file_path, clean=False)
        print(f"Top 10 characters in {lang} (before cleaning): {result[:10]}")
        print(f"Execution time: {exec_time:.2f} seconds\n")
        
        result_clean, exec_time_clean = count_characters(file_path, clean=True)
        print(f"Top 10 characters in {lang} (after cleaning): {result_clean[:10]}")
        print(f"Execution time: {exec_time_clean:.2f} seconds\n")