// AI Wellness Assistant - Simple JavaScript

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌟 AI Wellness Assistant - Simple UI Loaded');
    initializeApp();
});

// Main initialization
function initializeApp() {
    initializeTabs();
    initializeForms();
    setupEventListeners();
    
    // Show welcome message
    setTimeout(() => {
        showToast('Welcome to your AI Wellness Assistant!', 'success');
    }, 1000);
}

// Tab Management
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.nav-tab');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Remove active from all tabs
    document.querySelectorAll('.nav-tab').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Add active to selected tab
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

// Quick Track Functions
function quickTrack(habitType) {
    // Switch to track tab
    switchTab('track');
    
    // Pre-select habit type
    const habitSelect = document.getElementById('habit-type');
    if (habitSelect) {
        habitSelect.value = habitType;
        document.getElementById('habit-value').focus();
    }
    
    showToast(`Ready to track your ${habitType}!`, 'success');
}

// Form Handling
function initializeForms() {
    // Track form
    const trackForm = document.getElementById('track-form');
    if (trackForm) {
        trackForm.addEventListener('submit', handleTrackSubmit);
    }
    
    // Advice form
    const adviceForm = document.getElementById('advice-form');
    if (adviceForm) {
        adviceForm.addEventListener('submit', handleAdviceSubmit);
    }
    
    // Symptom form
    const symptomForm = document.getElementById('symptom-form');
    if (symptomForm) {
        symptomForm.addEventListener('submit', handleSymptomSubmit);
    }
}

async function handleTrackSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        habitType: formData.get('habit-type'),
        habitValue: formData.get('habit-value'),
        habitNotes: formData.get('habit-notes') || ''
    };
    
    if (!data.habitType || !data.habitValue) {
        showToast('Please fill in all required fields', 'error');
        return;
    }
    
    // Show loading
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    submitBtn.disabled = true;
    
    try {
        // Simulate API call
        await simulateAPICall('/api/track', data);
        
        // Success
        showToast(`${data.habitType} tracked successfully!`, 'success');
        e.target.reset();
        
        // Update summary if on dashboard
        if (document.getElementById('dashboard').classList.contains('active')) {
            loadSummary();
        }
        
    } catch (error) {
        showToast('Error saving habit. Please try again.', 'error');
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

async function handleAdviceSubmit(e) {
    e.preventDefault();
    
    const question = document.getElementById('advice-question').value.trim();
    if (!question) {
        showToast('Please enter a question', 'error');
        return;
    }
    
    const responseDiv = document.getElementById('advice-response');
    const contentDiv = document.getElementById('advice-content');
    
    // Show response area
    responseDiv.style.display = 'block';
    contentDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> AI is thinking...</div>';
    
    try {
        // Simulate AI response
        await simulateAPICall('/api/advice', { question });
        
        // Generate response based on question type
        const response = generateAdviceResponse(question);
        contentDiv.innerHTML = response;
        
        showToast('AI advice generated!', 'success');
        
    } catch (error) {
        contentDiv.innerHTML = '<p style="color: #dc3545;"><i class="fas fa-exclamation-triangle"></i> Sorry, I\'m having trouble right now. Please try again later.</p>';
        showToast('Error getting AI advice', 'error');
    }
}

async function handleSymptomSubmit(e) {
    e.preventDefault();
    
    const symptoms = document.getElementById('symptom-description').value.trim();
    const severity = parseInt(document.getElementById('symptom-severity').value);
    const duration = document.getElementById('symptom-duration').value;
    
    if (!symptoms || !duration) {
        showToast('Please fill in all required fields', 'error');
        return;
    }
    
    const responseDiv = document.getElementById('symptom-response');
    const contentDiv = document.getElementById('symptom-content');
    
    responseDiv.style.display = 'block';
    contentDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Analyzing symptoms...</div>';
    
    try {
        await simulateAPICall('/api/symptoms', { symptoms, severity, duration });
        
        const analysis = generateSymptomAnalysis(symptoms, severity, duration);
        contentDiv.innerHTML = analysis;
        
        showToast('Symptom analysis complete!', 'success');
        
    } catch (error) {
        contentDiv.innerHTML = '<p style="color: #dc3545;"><i class="fas fa-exclamation-triangle"></i> Error analyzing symptoms. Please try again.</p>';
        showToast('Error analyzing symptoms', 'error');
    }
}

// Event Listeners
function setupEventListeners() {
    // Severity slider
    const severitySlider = document.getElementById('symptom-severity');
    if (severitySlider) {
        severitySlider.addEventListener('input', function() {
            document.getElementById('severity-display').textContent = this.value;
        });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case '1':
                    e.preventDefault();
                    switchTab('dashboard');
                    break;
                case '2':
                    e.preventDefault();
                    switchTab('track');
                    break;
                case '3':
                    e.preventDefault();
                    switchTab('advice');
                    break;
            }
        }
    });
}

// Load Summary Function
async function loadSummary() {
    const summaryContent = document.getElementById('summary-content');
    if (!summaryContent) return;
    
    summaryContent.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    
    try {
        await simulateAPICall('/api/summary');
        
        // Generate realistic summary data
        const summaryData = generateSummaryData();
        
        summaryContent.innerHTML = summaryData.map(item => `
            <div class="summary-item">
                <span class="summary-label">${item.label}</span>
                <span class="summary-value">${item.value}</span>
            </div>
        `).join('');
        
        showToast('Summary refreshed!', 'success');
        
    } catch (error) {
        summaryContent.innerHTML = '<p style="color: #dc3545;">Error loading summary</p>';
        showToast('Error loading summary', 'error');
    }
}

// Utility Functions
function simulateAPICall(endpoint, data = null) {
    return new Promise((resolve, reject) => {
        // Simulate network delay
        const delay = Math.random() * 1000 + 500; // 500-1500ms
        
        setTimeout(() => {
            // Simulate occasional errors (5% chance)
            if (Math.random() < 0.05) {
                reject(new Error('Network error'));
            } else {
                resolve({ success: true, endpoint, data });
            }
        }, delay);
    });
}

function generateSummaryData() {
    const habits = ['Sleep', 'Water', 'Exercise', 'Mood'];
    const values = ['8 hours', '2.5 liters', '45 minutes', '8/10'];
    
    return habits.map((habit, index) => ({
        label: habit,
        value: values[index]
    }));
}

function generateAdviceResponse(question) {
    const lowerQuestion = question.toLowerCase();
    
    let response = `
        <p><strong>Based on your question: "${question.substring(0, 80)}${question.length > 80 ? '...' : ''}"</strong></p>
        <p>Here are some personalized recommendations:</p>
    `;
    
    if (lowerQuestion.includes('sleep')) {
        response += `
            <ul>
                <li>Maintain a consistent sleep schedule, going to bed and waking up at the same time daily</li>
                <li>Create a relaxing bedtime routine 30-60 minutes before sleep</li>
                <li>Keep your bedroom cool (60-67°F), dark, and quiet</li>
                <li>Limit screen time and caffeine before bedtime</li>
                <li>Consider natural sleep aids like chamomile tea or meditation</li>
            </ul>
        `;
    } else if (lowerQuestion.includes('exercise') || lowerQuestion.includes('workout')) {
        response += `
            <ul>
                <li>Start with 150 minutes of moderate-intensity exercise per week</li>
                <li>Include both cardio and strength training exercises</li>
                <li>Find activities you enjoy to make exercise sustainable</li>
                <li>Start slowly and gradually increase intensity</li>
                <li>Listen to your body and allow for rest days</li>
            </ul>
        `;
    } else if (lowerQuestion.includes('water') || lowerQuestion.includes('hydrat')) {
        response += `
            <ul>
                <li>Aim for 8-10 glasses (64-80 oz) of water daily</li>
                <li>Drink water first thing in the morning</li>
                <li>Carry a water bottle to track your intake</li>
                <li>Eat water-rich foods like fruits and vegetables</li>
                <li>Monitor urine color as a hydration indicator</li>
            </ul>
        `;
    } else if (lowerQuestion.includes('mood') || lowerQuestion.includes('stress')) {
        response += `
            <ul>
                <li>Practice mindfulness and deep breathing exercises</li>
                <li>Maintain social connections with friends and family</li>
                <li>Engage in regular physical activity</li>
                <li>Consider journaling to process emotions</li>
                <li>Seek professional help if mood concerns persist</li>
            </ul>
        `;
    } else {
        response += `
            <ul>
                <li>Focus on building consistent healthy habits</li>
                <li>Prioritize quality sleep, nutrition, and exercise</li>
                <li>Stay hydrated throughout the day</li>
                <li>Practice stress management techniques</li>
                <li>Regular check-ins with healthcare providers</li>
            </ul>
        `;
    }
    
    response += `
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin-top: 15px;">
            <p><strong><i class="fas fa-exclamation-triangle" style="color: #856404;"></i> Important:</strong> This is general wellness advice. For personalized medical guidance, please consult with healthcare professionals.</p>
        </div>
    `;
    
    return response;
}

function generateSymptomAnalysis(symptoms, severity, duration) {
    let analysis = `<p><strong>Symptom Analysis Summary:</strong></p>`;
    
    if (severity >= 8) {
        analysis += `
            <div class="alert alert-warning" style="margin: 15px 0;">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>High severity detected (${severity}/10).</strong> Please consider consulting a healthcare professional promptly.
            </div>
        `;
    } else if (severity >= 6) {
        analysis += `
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 15px 0;">
                <i class="fas fa-info-circle" style="color: #856404;"></i>
                <strong>Moderate severity (${severity}/10).</strong> Monitor closely and consider medical consultation if symptoms worsen.
            </div>
        `;
    }
    
    analysis += `<p><strong>General Recommendations:</strong></p><ul>`;
    
    if (duration === 'months' || severity >= 7) {
        analysis += `<li><strong>Seek medical attention</strong> - Long-duration or severe symptoms warrant professional evaluation</li>`;
    }
    
    analysis += `
        <li>Monitor your symptoms and note any changes</li>
        <li>Stay hydrated and get adequate rest</li>
        <li>Consider over-the-counter remedies if appropriate for your symptoms</li>
        <li>Maintain good nutrition to support your immune system</li>
        <li>Contact a healthcare provider if symptoms worsen or persist</li>
    </ul>`;
    
    if (symptoms.toLowerCase().includes('chest') || symptoms.toLowerCase().includes('breathing') || symptoms.toLowerCase().includes('heart')) {
        analysis += `
            <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 15px; margin: 15px 0; color: #721c24;">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>Important:</strong> Chest pain, breathing difficulties, or heart-related symptoms may require immediate medical attention. If severe, contact emergency services.
            </div>
        `;
    }
    
    analysis += `
        <div style="background: #d1ecf1; border: 1px solid #bee5eb; border-radius: 8px; padding: 15px; margin: 15px 0; color: #0c5460;">
            <p><strong><i class="fas fa-shield-alt"></i> Medical Disclaimer:</strong> This analysis is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.</p>
        </div>
    `;
    
    return analysis;
}

// Toast Notification Function
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
    };
    
    toast.innerHTML = `
        <i class="${icons[type] || icons.info}"></i>
        ${message}
    `;
    
    container.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Auto remove
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, 3000);
}

// Global functions for HTML onclick events
window.quickTrack = quickTrack;
window.loadSummary = loadSummary;
window.showToast = showToast;

console.log('🎉 AI Wellness Assistant - Simple UI Ready!');
