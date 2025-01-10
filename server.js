// server.js
const express = require('express');
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const app = express();

// Middleware for parsing form data
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Serve the HTML page
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Google Scraper</title>
    </head>
    <body>
      <h1>Google Scraper</h1>
      <form action="/search" method="POST">
        <label for="query">Enter search query:</label>
        <input type="text" id="query" name="query" required>
        <button type="submit">Search</button>
      </form>
    </body>
    </html>
  `);
});

// Handle the search and scraping
app.post('/search', async (req, res) => {
  const query = req.body.query;

  if (!query) {
    return res.status(400).send('Query is required');
  }

  try {
    // Launch Puppeteer browser
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Go to Google and perform search
    await page.goto(`https://www.google.com/search?q=${encodeURIComponent(query)}`);

    // Extract search results
    const results = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('div.yuRUbf > a'));
      return links.map(link => ({
        title: link.querySelector('h3')?.innerText || 'No title',
        url: link.href
      }));
    });

    await browser.close();

    // Save results to a JSON file
    const filePath = path.join(__dirname, 'results.json');
    fs.writeFileSync(filePath, JSON.stringify(results, null, 2));

    // Send file as response
    res.download(filePath, 'results.json', (err) => {
      if (err) {
        console.error(err);
      }
      fs.unlinkSync(filePath); // Delete the file after sending
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('An error occurred while processing your request.');
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
