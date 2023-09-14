// JavaScript code to combine key_counts.json files from the HotDog and ttztjohnsonm GitHub branches

// URLs of the raw key_counts.json files from different branches
const hotdogUrl = "https://raw.githubusercontent.com/ludothegreat/KeyCount/HotDog/key_counts.json";
const ttztjohnsonmUrl = "https://raw.githubusercontent.com/ludothegreat/KeyCount/ttztjohnsonm/key_counts.json";

// Function to combine key counts from multiple sources
function combineKeyCounts(data1, data2) {
    const combinedData = {};
    for (const category in data1) {
        combinedData[category] = { ...data1[category] };
        for (const key in data2[category]) {
            combinedData[category][key] = (combinedData[category][key] || 0) + data2[category][key];
        }
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
    summaryContainer.innerHTML = `<pre>${JSON.stringify(combinedData, null, 4)}</pre>`;
})
.catch(error => {
    console.error('An error occurred:', error);
});
