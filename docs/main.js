const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
const targetUrl = 'https://www.pexels.com/en-us/api/v3/sponsored-media/photos/car?number=4&page=1';

fetch(proxyUrl + targetUrl, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'secret-key': 'H2jk9uKnhRmL6WPwh89zBezWvr', // Make sure your key is valid
    }
})
    .then(response => response.json())
    .then(data => {
        document.getElementById('data').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('data').textContent = 'Failed to fetch data';
    });
