// src/apiLogic.js

// Fetch data from the API
const fetchData = async (number = 4, page = 1) => {
  try {
    const url = `https://www.pexels.com/en-us/api/v3/sponsored-media/photos/car?number=${number}&page=${page}`;

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

    return await response.json();
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
};

// Process the API response
const processAPIData = async (params) => {
  const { number, page } = params;

  // Fetch data using the fetchData function
  const data = await fetchData(number, page);

  // Log the data (replace this with any processing logic)
  console.log('API Response:', data);

  return data;
};

// Main function to handle API requests based on URL parameters
const main = async () => {
  const params = new URLSearchParams(window.location.search);
  const number = params.get('number') || 4; // Default: 4
  const page = params.get('page') || 1;    // Default: 1

  await processAPIData({ number, page });
};

// Run the main function
main();
