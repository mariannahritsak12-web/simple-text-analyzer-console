import pandas as pd
import string
import csv
import json
from matplotlib import pyplot as plt 
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from textblob import TextBlob


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
        text = text.lower()
        normalized_text = "".join(c for c in text if c not in string.punctuation)
        split_text = normalized_text.split()
        return split_text

    # Count words in the given text
    def count_words(self, text):
        stop_words = set(stopwords.words('english'))
        words = self._preprocess_text(text)
        filtered_words = [word for word in words if word not in stop_words]
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
        stop_words = set(stopwords.words('english'))
        clean_text = [word for word in words if word not in stop_words]
        top_words = {}

        for word in clean_text:
            if word not in top_words:
                top_words[word] = 0
            top_words[word] += 1

        return sorted(top_words.items(), key=lambda x: x[1], reverse=True)[:n]

    def top_words_pandas(self, text, n):
        df = pd.DataFrame(self._preprocess_text(text), columns=['word'])
        meaningful = df[df['word'].str.len() > 3]
        word_series = meaningful['word'].value_counts().head(n)
        return word_series.items()

    # Format the top words for better presentation
    def formatted_top_words(self, word_list):
        formatted = "".join(f"\n\t- {word}: {count}" for word, count in word_list)
        return formatted            

    def n_grams(self, text, n):
        words = self._preprocess_text(text)
        n_grams = zip(*[words[i:] for i in range(n)])
        return [" ".join(gram) for gram in n_grams]

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
    # Update this method to use pandas for better performance
    def unique_words(self, text):
        words = self._preprocess_text(text)
        unique_words = set()

        for word in words:
            if word not in unique_words:
                unique_words.add(word)
            
        return len(unique_words)

    # Generate report containing all information about proccessed text
    def generateReport(self, sentences, words, letters, top_words, avg_len, unique_words=None, lexical_diversity=None, sentiment=None):
        report = {
            'Sentences':sentences, 
            'Words':words, 
            'Letters':letters, 
            'Top Words':self.formatted_top_words(top_words), 
            'Average Word Length':avg_len,
            'Unique Words': unique_words,
            'Lexical Diversity': lexical_diversity,
            'Sentiment': sentiment
        }

        return report

    def lexical_diversity(self, text):
        words = self._preprocess_text(text)
        unique_words = set(words)
        return round(len(unique_words) / len(words), 2) if words else 0

    def sentiment_analysis(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment
        return f"Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}"

    # Export to csv
    def export_to_csv(self, report, filename):
        keys = report.keys()
        with open(filename, "w+", newline='', encoding='utf-8') as report_file:
            dict_writer = csv.DictWriter(report_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerow(report)
            
    def save_report_to_csv(self, df, filename):
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Report saved to {filename}")
    
    # Export to json
    def export_to_json(self, report, filename):
        with open(filename, "w+", encoding='utf-8') as report_file:
            json.dump(report, report_file, ensure_ascii=False, indent=4)

    def plot_word_frequencies(self, text, n):
        word_freq = dict(self.top_words_pandas(text, n))
        plt.bar(word_freq.keys(), word_freq.values())
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title('Top Word Frequencies')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def run_text_analyzer():
    path = input("Podaj ścieżkę do pliku tekstowego: ")
    analyzer = TextAnalyzer(path)

    sentences = analyzer.count_sentences(analyzer.text)
    words = analyzer.count_words(analyzer.text)
    letters = analyzer.count_letters(analyzer.text)
    top_words = analyzer.top_words(analyzer.text, 5)
    avg_len = analyzer.avg_word_len(analyzer.text)
    unique_words = analyzer.unique_words(analyzer.text)
    lexical_diversity = analyzer.lexical_diversity(analyzer.text)
    sentiment = analyzer.sentiment_analysis(analyzer.text)
    report = analyzer.generateReport(sentences , words, letters, top_words, avg_len, unique_words, lexical_diversity, sentiment)
    print("===REPORT===")
    for key, value in report.items():
        print(f"{key}: {value}")

    save_to_file = input("Do you want to save the report to a file? (yes/no): ")
    if save_to_file.lower() == "yes":
        output_filename = input("Enter file name: ")
        choice = input("Choose format (csv/json): ")
        if choice.lower() == "csv":
            analyzer.export_to_csv(report, output_filename)
        elif choice.lower() == "json":
            analyzer.export_to_json(report, output_filename)

if __name__ == "__main__":
    run_text_analyzer()