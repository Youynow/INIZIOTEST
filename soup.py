# Imports
from flask import Flask, request, render_template, jsonify, send_from_directory
import requests # http requests
from bs4 import BeautifulSoup # parsing html
import csv # write to csv

app = Flask(__name__) # initialize flask

@app.route('/')
def index():
    # define route for index.html
    return send_from_directory('.', 'index.html')

@app.route('/search', methods=['POST']) # for getting data from the html form
def search():
    query = request.form['query']
    # headers to mimic browser requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers) # use the requests library to get results
    soup = BeautifulSoup(response.text, 'html.parser') # parse html with bs

    # create results array
    results = []

    # iterate over the data
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else 'No title' # gets title
        link = g.find('a')['href'] if g.find('a') else 'No link' # get link
        description_tag = g.find('div', class_='VwiC3b') # try to get description of the result
        description = description_tag.text if description_tag else 'No description'
        results.append({'title': title, 'link': link, 'description': description})

    # save data to csv
    # open csv file
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['title', 'link', 'description']) # create writer
        writer.writeheader() 
        writer.writerows(results)

    #return jsonify(results) # display data on web

# Render the results on the page with the download link
    return render_template('search_results.html', query=query, results=results, file_path=file_path)

@app.route('/download')
def download_file():
    return send_from_directory('.', 'results.csv', as_attachment=True)

# debugging
if __name__ == '__main__':
    app.run(debug=True)
