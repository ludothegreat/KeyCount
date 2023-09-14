// JavaScript code to combine key_counts.json files from different GitHub branches

// URLs of the raw key_counts.json files from different branches
const mainUrl = "https://raw.githubusercontent.com/ludothegreat/KeyCount/main/key_counts.json";
const hotdogUrl = "https://raw.githubusercontent.com/ludothegreat/KeyCount/HotDog/key_counts.json";
const ttztjohnsonmUrl = "https://raw.githubusercontent.com/ludothegreat/KeyCount/ttztjohnsonm/key_counts.json";

// Function to combine key counts from multiple sources
function combineKeyCounts(mainData, additionalData) {
    for (const category in additionalData) {
        if (!mainData.hasOwnProperty(category)) {
            mainData[category] = {};
        }
        for (const key in additionalData[category]) {
            mainData[category][key] = (mainData[category][key] || 0) + additionalData[category][key];
        }
    }
    return mainData;
}

// Fetch and parse the key_counts.json data from each branch
Promise.all([
    fetch(mainUrl).then(response => response.json()),
    fetch(hotdogUrl).then(response => response.json()),
    fetch(ttztjohnsonmUrl).then(response => response.json())
])
.then(([mainData, hotdogData, ttztjohnsonmData]) => {
    // Combine the key counts
    const combinedData = combineKeyCounts(mainData, hotdogData);
    combineKeyCounts(combinedData, ttztjohnsonmData);

    // Display the combined data (for demonstration purposes, you can also save this to a file)
    const summaryContainer = document.getElementById('summary-container');
    summaryContainer.innerHTML = `<pre>${JSON.stringify(combinedData, null, 4)}</pre>`;
})
.catch(error => {
    console.error('An error occurred:', error);
});
