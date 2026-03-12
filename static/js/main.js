/**
 * Fake News and Review Detector — Main JavaScript
 * Handles detection logic, UI updates, and history management.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ---------------------------------------------------------
    //  INITIALIZATION
    // ---------------------------------------------------------
    
    // Auto-load history on history.html
    if (document.getElementById('historyGrid')) {
        loadHistory();
    }

    // Initialize Particles (if container exists)
    const particleEl = document.getElementById('particles-js');
    if (particleEl && typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', {
            particles: {
                number: { value: 60, density: { enable: true, value_area: 800 } },
                color: { value: '#00f2fe' },
                shape: { type: 'circle' },
                opacity: { value: 0.3, random: true },
                size: { value: 2, random: true },
                line_linked: { enable: true, distance: 150, color: '#a18cd1', opacity: 0.2, width: 1 },
                move: { enable: true, speed: 1.5, direction: 'none', random: true, straight: false, out_mode: 'out', bounce: false }
            },
            interactivity: {
                detect_on: 'canvas',
                events: { onhover: { enable: true, mode: 'grab' }, onclick: { enable: false } },
                modes: { grab: { distance: 140, line_linked: { opacity: 0.8 } } }
            },
            retina_detect: true
        });
    }

    // Counter Animation (Homepage)
    const counterEl = document.getElementById('accuracy-counter');
    if (counterEl) {
        let triggered = false;
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !triggered) {
                triggered = true;
                animateValue(counterEl, 80, 99.8, 2000);
            }
        }, { threshold: 0.5 });
        observer.observe(counterEl);
    }
});

/** Animate numerical values */
function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const val = progress * (end - start) + start;
        obj.innerHTML = val.toFixed(1) + (obj.dataset.suffix || '%');
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}


// ═════════════════════════════════════════════════════════════
//  DETECTION LOGIC (News & Review)
// ═════════════════════════════════════════════════════════════

/** Analyze news text */
function detectNews() {
    const text = document.getElementById('newsInput').value.trim();
    const resultBox = document.getElementById('newsResult');
    const analyzeBtn = document.querySelector('.btn-primary');

    if (!text) return alert("Please enter news text or headline.");

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = "ANALYZING...";
    resultBox.classList.remove('visible');

    fetch('/api/detect/news', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = "Analyze with AI";

        if (data.error) throw new Error(data.error);

        // Update UI
        const verdictEl = document.getElementById('newsVerdict');
        const confidenceEl = document.getElementById('newsConfidence');
        const bar = document.getElementById('newsProgressBar');
        const explanationEl = document.getElementById('newsExplanation');
        const sourcesEl = document.getElementById('newsSources');

        verdictEl.textContent = `${data.result} NEWS`;
        verdictEl.className = 'verdict ' + (data.result === 'FAKE' ? 'fake' : 'real');
        confidenceEl.textContent = `${data.confidence}% Accuracy Rating`;
        bar.style.width = data.confidence + '%';
        
        // Show explanation (if any)
        explanationEl.textContent = data.explanation || "No specific patterns detected.";

        // Real Source Verification
        sourcesEl.innerHTML = '';
        if (data.sources && data.sources.length > 0) {
            let html = '<h4>Real Source Verification</h4><ul>';
            data.sources.forEach(url => {
                html += `<li><a href="${url}" target="_blank">${new URL(url).hostname}</a></li>`;
            });
            html += '</ul>';
            sourcesEl.innerHTML = html;
        }

        resultBox.classList.add('visible');
    })
    .catch(err => {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = "Analyze with AI";
        alert("Error: " + err.message);
    });
}

/** Analyze product review */
function detectReview() {
    const text = document.getElementById('reviewInput').value.trim();
    const resultBox = document.getElementById('reviewResult');
    const analyzeBtn = document.querySelector('.btn-primary');

    if (!text) return alert("Please enter a review to analyze.");

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = "SCANNING...";
    resultBox.classList.remove('visible');

    fetch('/api/detect/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = "Detect Review Authenticity";

        if (data.error) throw new Error(data.error);

        const verdictEl = document.getElementById('reviewVerdict');
        const genuineBar = document.getElementById('probBarGenuine');
        const fakeBar = document.getElementById('probBarFake');
        const genuineVal = document.getElementById('probValGenuine');
        const fakeVal = document.getElementById('probValFake');

        const isFake = data.result === 'FAKE';
        verdictEl.textContent = isFake ? 'FAKE REVIEW' : 'GENUINE REVIEW';
        verdictEl.className = 'verdict ' + (isFake ? 'fake' : 'real');

        // Distribution
        const genuineProb = !isFake ? data.confidence : (100 - data.confidence).toFixed(1);
        const fakeProb = isFake ? data.confidence : (100 - data.confidence).toFixed(1);

        genuineBar.style.width = genuineProb + '%';
        fakeBar.style.width = fakeProb + '%';
        genuineVal.textContent = genuineProb + '%';
        fakeVal.textContent = fakeProb + '%';

        resultBox.classList.add('visible');
    })
    .catch(err => {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = "Detect Review Authenticity";
        alert("Error: " + err.message);
    });
}


// ═════════════════════════════════════════════════════════════
//  HISTORY DASHBOARD
// ═════════════════════════════════════════════════════════════

let historyData = [];
let currentFilter = 'all';

function loadHistory() {
    const grid = document.getElementById('historyGrid');
    if (!grid) return;

    grid.innerHTML = '<div class="empty-state"><i>⌛</i><p>Decrypting detection logs...</p></div>';

    fetch('/api/history')
        .then(res => res.json())
        .then(rows => {
            historyData = rows;
            updateHistoryStats(rows);
            renderHistoryGrid(rows);
        })
        .catch(err => {
            grid.innerHTML = `<div class="empty-state"><i>❌</i><p>Failed to load history: ${err.message}</p></div>`;
        });
}

function updateHistoryStats(rows) {
    const total = rows.length;
    const fake = rows.filter(r => r.result === 'FAKE').length;
    const real = rows.filter(r => r.result === 'REAL').length;

    const totalEl = document.getElementById('count-total');
    const fakeEl = document.getElementById('count-fake');
    const realEl = document.getElementById('count-real');

    if (totalEl) animateCount(totalEl, 0, total, 1000);
    if (fakeEl) animateCount(fakeEl, 0, fake, 1000);
    if (realEl) animateCount(realEl, 0, real, 1000);
}

function animateCount(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function setFilter(val) {
    currentFilter = val;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === val);
    });
    filterHistory();
}

function filterHistory() {
    const query = document.getElementById('historySearch').value.toLowerCase();
    
    const filtered = historyData.filter(r => {
        const matchesFilter = currentFilter === 'all' || r.result.toLowerCase() === currentFilter;
        const text = (r.input_text || r.image_filename || '').toLowerCase();
        const matchesSearch = text.includes(query);
        return matchesFilter && matchesSearch;
    });

    renderHistoryGrid(filtered);
}

function renderHistoryGrid(rows) {
    const grid = document.getElementById('historyGrid');
    if (!grid) return;

    if (!rows.length) {
        grid.innerHTML = '<div class="empty-state"><i>🔍</i><p>No matching records found.</p></div>';
        return;
    }

    const typeIcons = { news: '📰', review: '⭐', image: '🖼️' };

    grid.innerHTML = rows.map((r, index) => {
        const isFake = r.result === 'FAKE';
        const classType = isFake ? 'fake' : 'real';
        const icon = typeIcons[r.detection_type] || '❓';
        const preview = r.input_text || r.image_filename || 'No content';
        
        return `
            <div class="history-card ${classType} fade-in" style="animation-delay: ${index * 0.03}s">
                <div class="card-header">
                    <span class="type-tag">${icon} ${r.detection_type}</span>
                    <span class="result-badge ${classType}">${r.result} ${isFake ? '❌' : '✅'}</span>
                </div>
                
                <div class="card-content">
                    <div class="input-preview">"${preview}"</div>
                </div>
                
                <div class="confidence-section">
                    <div class="confidence-label">
                        <span>AI Confidence</span>
                        <span>${r.confidence}%</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: ${r.confidence}%"></div>
                    </div>
                </div>
                
                <div class="card-footer">
                    <span>#${r.id}</span>
                    <span>${r.created_at}</span>
                </div>
            </div>
        `;
    }).join('');
}


// ═════════════════════════════════════════════════════════════
//  UTILITIES
// ═════════════════════════════════════════════════════════════

function clearInput(inputId, resultId) {
    const inp = document.getElementById(inputId);
    if (inp) inp.value = '';

    const res = document.getElementById(resultId);
    if (res) {
        res.classList.remove('visible');
    }
}

function insertExample(inputId, text) {
    const inp = document.getElementById(inputId);
    if (inp) {
        inp.value = text;
        inp.focus();
    }
}
