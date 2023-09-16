// JavaScript code to combine key_counts.json files from the HotDog and ttztjohnsonm GitHub branches

// Function to display key counts in a readable format using a table
function displayReadableSummary(data) {
    const summaryContainer = document.getElementById('summary-container');
    summaryContainer.innerHTML = ''; // Clear previous content

    const table = document.createElement('table');
    table.style.width = '50%';
    table.setAttribute('border', '.5');

    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const keyHeader = document.createElement('th');
    keyHeader.textContent = 'Key';
    const countHeader = document.createElement('th');
    countHeader.textContent = 'Count';
    headerRow.appendChild(keyHeader);
    headerRow.appendChild(countHeader);
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');

    for (const key in data) {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        const countCell = document.createElement('td');
        countCell.textContent = data[key];
        row.appendChild(keyCell);
        row.appendChild(countCell);
        tbody.appendChild(row);
    }

    table.appendChild(tbody);
    summaryContainer.appendChild(table);
}


// URLs of the raw key_counts.json files from different branches
const hotdogUrl = "https://raw.githubusercontent.com/ludothegreat/KeyCount/HotDog/key_counts.json";
const ttztjohnsonmUrl = "https://raw.githubusercontent.com/ludothegreat/KeyCount/ttztjohnsonm/key_counts.json";

// Function to combine key counts from multiple sources
function combineKeyCounts(data1, data2) {
    const combinedData = { ...data1 };
    for (const key in data2) {
        combinedData[key] = (combinedData[key] || 0) + data2[key];
    }
    return combinedData;
}

// Fetch and parse the key_counts.json data from each branch
Promise.all([
    fetch(hotdogUrl).then(response => response.json()),
    fetch(ttztjohnsonmUrl).then(response => response.json())
])
.then(([hotdogData, ttztjohnsonmData]) => {
    // Combine the key counts
    const combinedData = combineKeyCounts(hotdogData, ttztjohnsonmData);

    // Display the combined data (for demonstration purposes, you can also save this to a file)
    const summaryContainer = document.getElementById('summary-container');
    displayReadableSummary(combinedData);})
.catch(error => {
    console.error('An error occurred:', error);
});
