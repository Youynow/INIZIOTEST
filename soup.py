from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)

@app.route('/')
def index():
    # Slouží k vrácení index.html
    return send_from_directory('.', 'index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else 'No title'
        link = g.find('a')['href'] if g.find('a') else 'No link'
        description = g.find('span', class_='aCOpRe').text if g.find('span', class_='VwiC3b') else 'No description'
        results.append({'title': title, 'link': link, 'description': description})

    # Uložení výsledků do CSV
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['title', 'link', 'description'])
        writer.writeheader()
        writer.writerows(results)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
