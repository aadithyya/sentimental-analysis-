
const reviewInput = document.getElementById('reviewInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = analyzeBtn.querySelector('.btn-text');
const spinner = analyzeBtn.querySelector('.spinner');

const errorMessage = document.getElementById('errorMessage');
const resultSection = document.getElementById('resultSection');

const resultEmoji = document.getElementById('resultEmoji');
const resultLabel = document.getElementById('resultLabel');
const resultConfidence = document.getElementById('resultConfidence');

const positiveBar = document.getElementById('positiveBar');
const negativeBar = document.getElementById('negativeBar');
const positiveValue = document.getElementById('positiveValue');
const negativeValue = document.getElementById('negativeValue');

const historyList = document.getElementById('historyList');

const MIN_LENGTH = 5;

function showError(message) {
    if (!message) {
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';
        return;
    }
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}



function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    btnText.textContent = isLoading ? 'Analyzing...' : 'Analyze Sentiment';
    spinner.classList.toggle('hidden', !isLoading);
}

function displayResult(data) {
    resultEmoji.textContent = data.emoji || '';

    
    const sentimentText = data.sentiment
        ? data.sentiment.charAt(0).toUpperCase() + data.sentiment.slice(1)
        : '';
    resultLabel.textContent = sentimentText;
    resultConfidence.textContent = `Confidence: ${data.confidence}%`;

    const positivePct = data.probabilities ? data.probabilities.positive : 0;
    const negativePct = data.probabilities ? data.probabilities.negative : 0;

    positiveBar.style.width = `${positivePct}%`;
    negativeBar.style.width = `${negativePct}%`;
    positiveValue.textContent = `${positivePct}%`;
    negativeValue.textContent = `${negativePct}%`;

    resultSection.classList.remove('hidden');
}


function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


async function loadHistory() {
    try {
        const response = await fetch('/history');
        if (!response.ok) return; 

        const data = await response.json();
        const items = data.history || [];

        if (items.length === 0) {
            historyList.innerHTML = '<li class="empty-state">No analyses yet — try one above!</li>';
            return;
        }

        historyList.innerHTML = items.map((item) => `
            <li>
                <span>
                    <span class="history-review">${escapeHtml(item.review)}</span>
                    <span class="history-meta">${escapeHtml(item.timestamp)}</span>
                </span>
                <span class="history-sentiment ${item.sentiment.toLowerCase()}">
                    ${item.sentiment} (${item.confidence}%)
                </span>
            </li>
        `).join('');
    } catch (err) {
     
        console.error('Could not load history:', err);
    }
}


async function handleAnalyzeClick() {
    const text = reviewInput.value.trim();

    showError(null);
    resultSection.classList.add('hidden');

    if (!text) {
        showError('Please enter a review to analyze.');
        return;
    }
    if (text.length < MIN_LENGTH) {
        showError(`Review must be at least ${MIN_LENGTH} characters long.`);
        return;
    }

    setLoading(true);

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || 'Something went wrong. Please try again.');
            return;
        }

        displayResult(data);
        loadHistory(); 
    } catch (err) {
        showError('Could not reach the server. Is it running?');
    } finally {
        setLoading(false);
    }
}

analyzeBtn.addEventListener('click', handleAnalyzeClick);


document.addEventListener('DOMContentLoaded', loadHistory);