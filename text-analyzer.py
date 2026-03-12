from fileinput import filename
import string
import csv
import os


# Load the text from the specified file
def load_text(file_location):
    with open(file_location, "r") as text_file:
        return text_file.read()

# Remove the punctuation characters
def clean_text(text):
    text = text.lower()
    clean_text = "".join(c for c in text if c not in string.punctuation)

    return clean_text

# Count words in the given text
def count_words(text):
    return len(text.split())

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