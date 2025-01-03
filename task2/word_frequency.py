import requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re

def fetch_text(url):
    """Завантажує текст із заданої URL-адреси."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def map_function(chunk):
    """Розбиває текст на слова і повертає словник з частотами."""
    words = re.findall(r'\b\w+\b', chunk.lower())
    return Counter(words)

def reduce_function(counters):
    """Об'єднує кілька Counter-об'єктів у один."""
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter

def split_text(text, num_chunks):
    """Розбиває текст на кілька частин для обробки."""
    chunk_size = len(text) // num_chunks
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def analyze_word_frequencies(text, num_threads=4):
    """Аналізує частоту слів у тексті за допомогою MapReduce."""
    chunks = split_text(text, num_threads)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        mapped = list(executor.map(map_function, chunks))
    return reduce_function(mapped)

def visualize_top_words(word_counts, top_n=10):
    """Візуалізує топ слів із найвищою частотою."""
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top 10 Most Frequent Words")
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == "__main__":
    # URL-адреса тексту (замініть на потрібний URL)
    url = "https://www.gutenberg.org/files/1342/1342-0.txt" 

    try:
        text = fetch_text(url)
        word_counts = analyze_word_frequencies(text)
        visualize_top_words(word_counts)
    except requests.exceptions.RequestException as e:
        print(f"Помилка завантаження тексту: {e}")
