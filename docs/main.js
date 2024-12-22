// Fetch data from the Pexels API using the GET request with headers
fetch('https://www.pexels.com/en-us/api/v3/sponsored-media/photos/car?number=4&page=1', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'secret-key': 'H2jk9uKnhRmL6WPwh89zBezWvr'
    }
})
    .then(response => response.json()) // Parse the response to JSON
    .then(data => {
        // Display the raw data inside the 'data' div
        document.getElementById('data').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('data').textContent = 'Failed to fetch data';
    });
