const express = require('express');
const fetch = require('node-fetch'); // For making API requests

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to add CORS headers
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', 'https://www.pexels.com/search/car/'); // Allow all origins
  res.setHeader('Access-Control-Allow-Methods', 'GET'); // Allow specific methods
  // Allow specific headers
  next();
});

// Route to handle requests and fetch data from the external API
app.get('/api/photos', async (req, res) => {
  const { number = 4, page = 1 } = req.query;

  const url = `https://www.pexels.com/en-us/api/v3/sponsored-media/photos/car?number=${number}&page=${page}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'secret-key': 'H2jk9uKnhRmL6WPwh89zBezWvr',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    res.status(200).json(data); // Send the JSON response to the client
  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).json({ error: 'Failed to fetch data from the external API' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
