import string
import csv

class TextAnalyzer:
    def __init__(self, file_location):
        self.file_location = file_location
        self.text = self._load_text()
        self.clean_text = self._preprocess_text(self.text)

    # Load the text from the specified file
    def _load_text(self):
        try:  
            with open(self.file_location, "r", encoding='utf-8') as text_file:
                return text_file.read()
        except FileNotFoundError:
            print(f'Nie można znaleźć pliku: {self.file_location}')
            return ""

    # Split the text into words, remove punctuation and convert to lowercase
    def _preprocess_text(self, text):
        text = self.text.lower()
        normalized_text = "".join(c for c in text if c not in string.punctuation)
        split_text = normalized_text.split()
        return split_text

    # Count words in the given text
    def count_words(self, text):
        STOP_WORDS = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'while', 'with', 'to', 'of'}
        words = self._preprocess_text(text)
        filtered_words = [word for word in words if word not in STOP_WORDS]
        return len(filtered_words)

    # Count letters
    def count_letters(self, text):
        letters = 0
        for char in text:
            if char.isalpha():
                letters += 1
        return letters

    # Word frequency
    def top_words(self, text, n):
        words = self._preprocess_text(text)
        top_words = {}

        for word in words:
            if word not in top_words:
                top_words[word] = 0
            top_words[word] += 1

        return sorted(top_words.items(), key=lambda x: x[1], reverse=True)[:n]

    # Format the top words for better presentation
    def formatted_top_words(self, word_list):
        formatted = "".join(f"\n\t- {word}: {count}" for word, count in word_list)
        return formatted            

    # Average words lenghth
    def avg_word_len(self, text):
        words = self._preprocess_text(text)
        total_lenghth = 0

        for word in words:
            total_lenghth += len(word)
        
        return round(total_lenghth / len(words), 2) if words else 0

    # Count the number of sentences in the text
    def count_sentences(self, text):
        sentence_endings = ['.', '!', '?']
        sentences = 0
        
        for char in text:
            if char in sentence_endings:
                sentences += 1

        return sentences

    # Unique words in the text
    def unique_words(self, text):
        words = self._preprocess_text(text)
        unique_words = set()

        for word in words:
            if word not in unique_words:
                unique_words.add(word)
            
        return len(unique_words)

    # Generate report containing all information about proccessed text
    def generateReport(self, sentences, words, letters, top_words, avg_len):
        report = {
            'Sentences':sentences, 'Words':words, 'Letters':letters, 'Top Words':self.formatted_top_words(top_words), 
            'Average Word Length':avg_len
        }

        return report

    # Export to csv
    def export_to_csv(self, report, filename):
        keys = report.keys()
        with open(filename, "w+", newline='', encoding='utf-8') as report_file:
            dict_writer = csv.DictWriter(report_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerow(report)
            

def run_text_analyzer():
    path = input("Podaj ścieżkę do pliku tekstowego: ")
    analyzer = TextAnalyzer(path)

    sentences = analyzer.count_sentences(analyzer.text)
    words = analyzer.count_words(analyzer.text)
    letters = analyzer.count_letters(analyzer.text)
    top_words = analyzer.top_words(analyzer.text, 5)
    avg_len = analyzer.avg_word_len(analyzer.text)
    unique_words = analyzer.unique_words(analyzer.text)
    report = analyzer.generateReport(sentences , words, letters, top_words, avg_len)
    print("===REPORT===")
    for key, value in report.items():
        print(f"{key}: {value}")

    save_as_csv = input("Czy chcesz zapisać raport do pliku CSV? (tak/nie): ")
    if save_as_csv.lower() == "tak":
        output_filename = input("Podaj nazwę pliku CSV (np. raport.csv): ")
        analyzer.export_to_csv(report, output_filename)

if __name__ == "__main__":
    run_text_analyzer()