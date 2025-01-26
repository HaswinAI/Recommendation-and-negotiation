// Function to append a new response below the previous one
function appendResponse(responseContent) {
    const analysisContainer = document.getElementById('analysis');
    const responseDiv = document.createElement('div');
    responseDiv.classList.add('response');
    responseDiv.innerHTML = responseContent;
    analysisContainer.appendChild(responseDiv);
}

// Event listener for the submit button
document.getElementById('submitBtn').addEventListener('click', async () => {
    const userText = document.getElementById('userText').value;
    if (!userText) {
        alert("Please enter a message!");
        return;
    }

    // Send the user text to the backend for processing
    const response = await fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: userText })
    });

    const data = await response.json();
    if (data.response) {
        appendResponse(`<h2>Analysis Complete!</h2><ul><li>${data.response}</li></ul>`);
    } else {
        appendResponse(`<h2>Error:</h2><ul><li>${data.error}</li></ul>`);
    }
});

// Event listener for the fetch summary button
document.getElementById('fetchSummaryBtn').addEventListener('click', async () => {
    const response = await fetch('/fetch_summary', { method: 'GET' });
    const data = await response.json();

    const outputDiv = document.getElementById('summaryOutput');

    if (data.summary) {
        // Preserve formatting by wrapping the summary in <pre> tags
        outputDiv.innerHTML = `<pre>${data.summary}</pre>`;
    } else {
        outputDiv.innerHTML = `<p>${data.error}</p>`;
    }
});

// Event listener for the negotiation button
document.getElementById('negotiateBtn').addEventListener('click', async () => {
    const negotiateText = document.getElementById('negotiateText').value;
    if (!negotiateText) {
        alert("Please enter your negotiation input!");
        return;
    }

    // Send the user text to the backend for negotiation coaching
    const response = await fetch('/negotiate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: negotiateText })
    });

    const data = await response.json();
    if (data.suggestion) {
        document.getElementById('negotiationSuggestion').innerHTML = `<h3>Negotiation Suggestion:</h3><p>${data.suggestion}</p>`;
    } else {
        document.getElementById('negotiationSuggestion').innerHTML = `<p>${data.error}</p>`;
    }
});
