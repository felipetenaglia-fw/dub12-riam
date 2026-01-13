// Student Dashboard JavaScript
let currentPage = 'dashboard';
let studentData = {
    name: "Emma Johnson",
    module: "Advanced Piano Performance",
    teacher: "Ms. Anderson",
    overallScore: 78,
    dimensions: {
        technical: 82,
        musicianship: 75,
        repertoire: 70,
        artistry: 85
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeStudent();
    setupEventListeners();
    createCharts();
});

function initializeStudent() {
    showPage('dashboard');
    updateProgressCircle();
}

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            showPage(page);
            updateActiveNav(this);
        });
    });

    // Assignment filters
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterAssignments(this.getAttribute('data-filter'));
        });
    });

    // File upload
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    
    if (fileInput && uploadArea) {
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('drop', handleFileDrop);
        fileInput.addEventListener('change', handleFileSelect);
    }

    // AI Chat
    const aiChatInput = document.getElementById('aiChatInput');
    if (aiChatInput) {
        aiChatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendAIMessage();
            }
        });
    }
}

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
        currentPage = pageId;
    }
}

function updateActiveNav(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

function updateProgressCircle() {
    const canvas = document.getElementById('progressChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 45;
    const progress = studentData.overallScore / 100;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Background circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 8;
    ctx.stroke();
    
    // Progress arc
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, -Math.PI / 2, -Math.PI / 2 + (2 * Math.PI * progress));
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 8;
    ctx.lineCap = 'round';
    ctx.stroke();
}

function createCharts() {
    createProgressTimeChart();
}

function createProgressTimeChart() {
    const canvas = document.getElementById('progressTimeChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
            datasets: [{
                label: 'Technical Skills',
                data: [70, 73, 76, 79, 82],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4
            }, {
                label: 'Musicianship',
                data: [65, 68, 70, 72, 75],
                borderColor: '#38b2ac',
                backgroundColor: 'rgba(56, 178, 172, 0.1)',
                tension: 0.4
            }, {
                label: 'Repertoire',
                data: [60, 63, 66, 68, 70],
                borderColor: '#ed8936',
                backgroundColor: 'rgba(237, 137, 54, 0.1)',
                tension: 0.4
            }, {
                label: 'Artistry',
                data: [75, 78, 80, 83, 85],
                borderColor: '#e53e3e',
                backgroundColor: 'rgba(229, 62, 62, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 50,
                    max: 100
                }
            }
        }
    });
}

// Assignment Functions
function filterAssignments(filter) {
    const assignments = document.querySelectorAll('.assignment-card');
    assignments.forEach(assignment => {
        if (filter === 'all' || assignment.classList.contains(filter)) {
            assignment.style.display = 'block';
        } else {
            assignment.style.display = 'none';
        }
    });
}

function startAssignment(assignmentId) {
    alert(`Starting assignment ${assignmentId}. This would open the assignment interface.`);
}

function acceptAIAssignment(assignmentId) {
    const assignmentCard = event.target.closest('.assignment-card');
    assignmentCard.classList.remove('ai-generated');
    assignmentCard.classList.add('pending');
    
    const statusElement = assignmentCard.querySelector('.assignment-status') || 
                         document.createElement('div');
    statusElement.className = 'assignment-status pending';
    statusElement.textContent = 'Pending';
    
    if (!assignmentCard.querySelector('.assignment-status')) {
        assignmentCard.appendChild(statusElement);
    }
    
    // Replace actions
    const actionsDiv = assignmentCard.querySelector('.assignment-actions');
    actionsDiv.innerHTML = '<button class="btn-primary" onclick="startAssignment(1)">Start Assignment</button>';
    
    showNotification('AI assignment accepted and added to your pending assignments!');
}

function declineAIAssignment(assignmentId) {
    const assignmentCard = event.target.closest('.assignment-card');
    assignmentCard.style.display = 'none';
    showNotification('AI assignment declined.');
}

// File Upload Functions
function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
}

function handleFileDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    handleFiles(files);
}

function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    if (files.length > 0) {
        document.getElementById('uploadArea').style.display = 'none';
        document.getElementById('submissionForm').style.display = 'block';
        
        // Show file info
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';
        fileInfo.innerHTML = `
            <i class="fas fa-file"></i>
            <span>${files[0].name}</span>
            <small>${(files[0].size / 1024 / 1024).toFixed(2)} MB</small>
        `;
        document.getElementById('submissionForm').prepend(fileInfo);
    }
}

function submitAssignment() {
    // Simulate submission
    showNotification('Assignment submitted successfully!');
    
    // Reset form
    document.getElementById('submissionForm').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'block';
    
    // Add to submissions history
    addToSubmissionHistory();
}

function cancelSubmission() {
    document.getElementById('submissionForm').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'block';
    
    const fileInfo = document.querySelector('.file-info');
    if (fileInfo) fileInfo.remove();
}

function addToSubmissionHistory() {
    const historyContainer = document.querySelector('.submissions-history');
    const newSubmission = document.createElement('div');
    newSubmission.className = 'submission-item';
    newSubmission.innerHTML = `
        <div class="submission-info">
            <i class="fas fa-video"></i>
            <div>
                <h4>New Assignment Submission</h4>
                <p>Submitted: Just now • Grade: Pending</p>
            </div>
        </div>
        <div class="submission-actions">
            <button class="btn-outline">View</button>
        </div>
    `;
    
    const existingSubmissions = historyContainer.querySelector('.submission-item');
    if (existingSubmissions) {
        historyContainer.insertBefore(newSubmission, existingSubmissions);
    } else {
        historyContainer.appendChild(newSubmission);
    }
}

// AI Chat Functions
function sendAIMessage() {
    const input = document.getElementById('aiChatInput');
    const chatMessages = document.getElementById('aiChatMessages');
    
    if (!input.value.trim()) return;
    
    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.innerHTML = `
        <div class="message-content">
            <p>${input.value}</p>
        </div>
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
    `;
    chatMessages.appendChild(userMessage);
    
    const userInput = input.value;
    input.value = '';
    
    // Simulate AI response
    setTimeout(() => {
        const aiResponse = generateAIResponse(userInput);
        const aiMessage = document.createElement('div');
        aiMessage.className = 'ai-message';
        aiMessage.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <p>${aiResponse}</p>
            </div>
        `;
        chatMessages.appendChild(aiMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function generateAIResponse(userInput) {
    const input = userInput.toLowerCase();
    
    if (input.includes('practice') || input.includes('practicing')) {
        return "Great question about practice! Based on your recent progress, I recommend focusing on slow practice with the metronome. Your rhythm accuracy has improved 15% this week, which is excellent! Try practicing your scales at 60 BPM and gradually increase the tempo.";
    } else if (input.includes('technique') || input.includes('technical')) {
        return "Your technical skills are at 82%, which is very strong! I notice you're excelling in finger independence. To improve further, focus on pedaling coordination - this came up in your teacher's recent feedback. Try the pedaling exercises I've added to your assignments.";
    } else if (input.includes('assignment') || input.includes('homework')) {
        return "You have 2 pending assignments: Scale Practice and the AI-generated Dynamics Exercise. I recommend starting with the scale practice as it will help with your technical foundation. Would you like me to break down the practice steps for you?";
    } else if (input.includes('performance') || input.includes('recital')) {
        return "Your performance artistry score of 85% is exceptional! You have natural stage presence and musical expression. For your next performance, consider working on dynamic contrasts to make your interpretation even more compelling.";
    } else if (input.includes('help') || input.includes('stuck')) {
        return "I'm here to help! You can ask me about your practice routine, specific techniques, assignment guidance, or performance preparation. I can also analyze your progress and suggest personalized exercises. What specific area would you like help with?";
    } else {
        return "That's an interesting question! Based on your current progress (78% overall), you're doing really well. Your strongest area is Performance Artistry (85%) and there's room for growth in Repertoire Knowledge (70%). Keep up the great work, and remember that consistent practice is key to improvement!";
    }
}

// Module Functions
function viewModule(moduleId) {
    showNotification('Opening module details...');
    // This would navigate to detailed module view
}

// Utility Functions
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #667eea;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function logout() {
    localStorage.removeItem('userRole');
    window.location.href = 'index.html';
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .drag-over {
        border-color: #667eea !important;
        background-color: rgba(102, 126, 234, 0.1) !important;
    }
    
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
    }
    
    .user-message .message-content {
        background: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 12px 12px 4px 12px;
        max-width: 70%;
    }
    
    .user-message .message-avatar {
        margin-left: 0.5rem;
        width: 30px;
        height: 30px;
        background: #667eea;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }
`;
document.head.appendChild(style);