// Fetch data from the API and display it in the 'data' div
fetch('https://raw.githubusercontent.com/myapihidenowfromanycost/Api/refs/heads/master/tts/lts.json')
    .then(response => response.json()) // Convert the response to JSON
    .then(data => {
        // Display the raw data inside the 'data' div
        document.getElementById('data').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('data').textContent = 'Failed to fetch data';
    });
