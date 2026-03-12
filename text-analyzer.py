import string
import csv
import os

# Load the text from the specified file
def load_text(file_location):
    with open(file_location, "r") as text_file:
        return text_file.read()

# Split the text into words, remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.lower()
    normalized_text = "".join(c for c in text if c not in string.punctuation)
    split_text = normalized_text.split()
    return split_text

# Count words in the given text
def count_words(text):
    STOP_WORDS = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'while', 'with', 'to', 'of'}
    words = preprocess_text(text)
    filtered_words = [word for word in words if word not in STOP_WORDS]
    return len(filtered_words)

# Count letters
def count_letters(text):
    letters = 0
    for char in text:
        if char.isalpha():
            letters += 1
    return letters

# Word frequency
def top_words(text, n):
    words = text.lower().split()
    top_words = {}

    for word in words:
        if word not in top_words:
            top_words[word] = 0
        top_words[word] += 1

    return sorted(top_words.items(), key=lambda x: x[1], reverse=True)[:n]

# Average words lenghth
def avg_word_len(text):
    words = text.split()
    total_lenghth = 0

    for word in words:
        total_lenghth += len(word)
    
    return total_lenghth / len(words)

# Count the number of sentences in the text
def count_sentences(text):
    sentence_endings = ['.', '!', '?']
    sentences = 0
    
    for char in text:
      if char in sentence_endings:
          sentences += 1

    return sentences

# Unique words in the text
def unique_words():
    words = preprocess_text(text)
    unique_words = set()

    for word in words:
        if word not in unique_words:
            unique_words.add(word)
        
    return len(unique_words)

# Generate report containing all information about proccessed text
def generateReport(words, letters, top_words, avg_len):
    report = {
        'Words':words, 'Letters':letters, 'Top Words':top_words, 
        'Average Word Length':avg_len
    }

    return report

# Export to csv
def export_to_csv(report, filename):
    keys = report.keys()
    with open(filename, "w+", newline='', encoding='utf-8') as report_file:
        dict_writer = csv.DictWriter(report_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerow(report)
        

# Main function
if __name__ == "__main__":
    path = input('Podaj ścieżke do pliku tekstowego:')
    text = load_text(path)
    clean = clean_text(text)
    words = count_words(clean)
    letters = count_letters(clean)
    top = top_words(clean, 10)
    avg_len = avg_word_len(clean)
    report = generateReport(words, letters, top, avg_len)
    export_to_csv(report, 'report.csv')