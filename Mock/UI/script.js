// Mock Data
const mockStudents = [
    {
        id: 1,
        name: "Emma Johnson",
        grade: "Grade 6 Piano",
        startDate: "Sept 2023",
        overallScore: 78,
        dimensions: {
            technical: 82,
            musicianship: 75,
            repertoire: 70,
            artistry: 85
        },
        assignments: [
            { id: 1, title: "Practice scales - C major, 2 octaves", status: "pending" },
            { id: 2, title: "Record Chopin Waltz performance", status: "completed" }
        ],
        recentActivity: [
            { action: "Completed Bach Invention No. 1", time: "2 hours ago", icon: "fas fa-music" },
            { action: "Received teacher feedback", time: "1 day ago", icon: "fas fa-comment" }
        ]
    },
    {
        id: 2,
        name: "James Wilson",
        grade: "Grade 4 Violin",
        startDate: "Jan 2024",
        overallScore: 65,
        dimensions: {
            technical: 60,
            musicianship: 68,
            repertoire: 62,
            artistry: 70
        },
        assignments: [
            { id: 3, title: "Work on bow technique exercises", status: "pending" },
            { id: 4, title: "Learn Mozart Sonata K.301", status: "pending" }
        ],
        recentActivity: [
            { action: "Practiced scales exercise", time: "4 hours ago", icon: "fas fa-music" },
            { action: "Uploaded practice video", time: "2 days ago", icon: "fas fa-video" }
        ]
    }
];

const mockTeacherComments = [
    "Excellent technical progress, but needs work on musical expression",
    "Strong rhythmic accuracy, focus on dynamic contrast",
    "Good finger technique, improve pedaling skills",
    "Outstanding performance quality, minor intonation issues",
    "Solid understanding of theory, practice sight-reading more"
];

const mockAIFeedback = [
    {
        category: "Technical Skills",
        score: 82,
        feedback: "Excellent finger independence and clarity. Minor timing inconsistencies in measures 12-16.",
        recommendations: ["Practice with metronome at 80 BPM", "Focus on left-hand articulation"]
    },
    {
        category: "Musical Expression",
        score: 75,
        feedback: "Good phrasing overall. Consider more dynamic contrast in the development section.",
        recommendations: ["Work on crescendo in measures 8-12", "Practice different touch techniques"]
    }
];

// Global State
let currentUser = 'student';
let currentStudent = mockStudents[0];
let isRecording = false;

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    updateProgressCircle();
});

function initializeApp() {
    showPage('dashboard');
    updateUserInterface();
    generateMockChart();
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

    // Chat input
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // AI Chat input
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
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // Update page-specific content
    if (pageId === 'passport') {
        updatePassportData();
    } else if (pageId === 'metrics') {
        updateMetricsData();
    } else if (pageId === 'ai-feedback') {
        updateAIFeedbackData();
    }
}

function updateActiveNav(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

function switchRole() {
    const roleSelect = document.getElementById('userRole');
    currentUser = roleSelect.value;
    updateUserInterface();
}

function updateUserInterface() {
    // Update content based on user role
    switch(currentUser) {
        case 'student':
            updateStudentView();
            break;
        case 'teacher':
            updateTeacherView();
            break;
        case 'admin':
            updateAdminView();
            break;
    }
}

function updateStudentView() {
    // Update dashboard for student
    const studentName = document.getElementById('studentName');
    if (studentName) {
        studentName.textContent = currentStudent.name;
    }
    
    const overallScore = document.getElementById('overallScore');
    if (overallScore) {
        overallScore.textContent = currentStudent.overallScore + '%';
    }
}

function updateTeacherView() {
    // Add teacher-specific content
    addTeacherAlerts();
}

function updateAdminView() {
    // Add admin-specific content
    addAdminMetrics();
}

function updatePassportData() {
    // Update student profile
    const studentName = document.getElementById('studentName');
    const overallScore = document.getElementById('overallScore');
    
    if (studentName) studentName.textContent = currentStudent.name;
    if (overallScore) overallScore.textContent = currentStudent.overallScore + '%';

    // Update dimension scores
    const dimensions = ['technical', 'musicianship', 'repertoire', 'artistry'];
    dimensions.forEach((dim, index) => {
        const scoreBar = document.querySelectorAll('.score-fill')[index];
        const scoreText = document.querySelectorAll('.score-text')[index];
        
        if (scoreBar && scoreText) {
            const score = currentStudent.dimensions[dim];
            scoreBar.style.width = score + '%';
            scoreText.textContent = score + '%';
        }
    });
}

function updateMetricsData() {
    // Generate random metrics for demo
    const practiceHours = (Math.random() * 30 + 15).toFixed(1);
    const completionRate = Math.floor(Math.random() * 30 + 70);
    const aiFeedbackScore = (Math.random() * 1.5 + 3.5).toFixed(1);

    // Update metric cards
    const metricValues = document.querySelectorAll('.metric-value');
    if (metricValues.length >= 3) {
        metricValues[0].textContent = practiceHours + 'h';
        metricValues[1].textContent = Math.floor(completionRate * 0.1) + '/10';
        metricValues[2].textContent = aiFeedbackScore + '/5';
    }
}

function updateAIFeedbackData() {
    // Update AI feedback with mock data
    const feedbackContent = document.querySelector('.feedback-content');
    if (feedbackContent) {
        // This would be populated with real AI analysis
        console.log('AI Feedback updated with latest analysis');
    }
}

function updateProgressCircle() {
    const circle = document.querySelector('.circle');
    if (circle) {
        const percent = currentStudent.overallScore;
        circle.style.setProperty('--percent', percent);
    }
}

// Communication Functions
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    
    if (messageInput && chatMessages && messageInput.value.trim()) {
        const message = createMessageElement(messageInput.value, 'student');
        chatMessages.appendChild(message);
        messageInput.value = '';
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Simulate teacher response after delay
        setTimeout(() => {
            const response = generateTeacherResponse();
            const teacherMessage = createMessageElement(response, 'teacher');
            chatMessages.appendChild(teacherMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 2000);
    }
}

function createMessageElement(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const now = new Date();
    const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <strong>${sender === 'student' ? 'You' : 'Ms. Anderson'}</strong>
            <span class="timestamp">Today, ${timeString}</span>
        </div>
        <p>${text}</p>
    `;
    
    return messageDiv;
}

function generateTeacherResponse() {
    const responses = [
        "Thank you for sharing your practice session. I can see improvement in your technique!",
        "Great work! Let's focus on the dynamics in the next lesson.",
        "I've reviewed your recording. Please work on the tempo consistency.",
        "Excellent progress! Keep up the good work with your daily practice.",
        "I notice some areas for improvement. Let's schedule a video call to discuss."
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
}

// AI Chat Functions
function sendAIMessage() {
    const aiChatInput = document.getElementById('aiChatInput');
    const aiChat = document.querySelector('.ai-chat');
    
    if (aiChatInput && aiChat && aiChatInput.value.trim()) {
        // Add user message
        const userMessage = document.createElement('div');
        userMessage.className = 'ai-message user';
        userMessage.innerHTML = `
            <i class="fas fa-user"></i>
            <div class="message-content">
                <p>${aiChatInput.value}</p>
            </div>
        `;
        aiChat.appendChild(userMessage);
        
        const userInput = aiChatInput.value;
        aiChatInput.value = '';
        
        // Simulate AI response
        setTimeout(() => {
            const aiResponse = generateAIResponse(userInput);
            const aiMessage = document.createElement('div');
            aiMessage.className = 'ai-message';
            aiMessage.innerHTML = `
                <i class="fas fa-robot"></i>
                <div class="message-content">
                    <p>${aiResponse}</p>
                </div>
            `;
            aiChat.appendChild(aiMessage);
            aiChat.scrollTop = aiChat.scrollHeight;
        }, 1500);
        
        aiChat.scrollTop = aiChat.scrollHeight;
    }
}

function generateAIResponse(userInput) {
    const input = userInput.toLowerCase();
    
    if (input.includes('technique') || input.includes('technical')) {
        return "Based on your recent recordings, your technical skills are strong at 82%. I recommend focusing on finger independence exercises and practicing scales at varying tempos to further improve.";
    } else if (input.includes('practice') || input.includes('practicing')) {
        return "Your practice consistency is excellent! I suggest incorporating more slow practice sessions and using a metronome for better timing accuracy.";
    } else if (input.includes('performance') || input.includes('performing')) {
        return "Your performance artistry scores are impressive at 85%! To enhance further, work on dynamic contrasts and emotional expression in your pieces.";
    } else if (input.includes('feedback') || input.includes('score')) {
        return "Your overall score of 78% shows great progress! Areas for improvement include repertoire knowledge (70%) and musicianship skills (75%). I've assigned specific exercises to help.";
    } else {
        return "I'm here to help with your musical development! Ask me about your technique, practice routine, performance skills, or any specific feedback on your progress.";
    }
}

// Recording Functions
function openRecordingModal() {
    const modal = document.getElementById('recordingModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeRecordingModal() {
    const modal = document.getElementById('recordingModal');
    if (modal) {
        modal.style.display = 'none';
    }
    
    // Stop recording if active
    if (isRecording) {
        toggleRecording();
    }
}

function toggleRecording() {
    const recordBtn = document.getElementById('recordBtn');
    const recordingStatus = document.getElementById('recordingStatus');
    
    if (!isRecording) {
        // Start recording
        isRecording = true;
        recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
        recordBtn.classList.add('recording');
        recordingStatus.textContent = 'Recording... Click stop when finished.';
        
        // Simulate recording process
        simulateRecording();
    } else {
        // Stop recording
        isRecording = false;
        recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
        recordBtn.classList.remove('recording');
        recordingStatus.textContent = 'Recording saved successfully!';
        
        // Close modal after delay
        setTimeout(() => {
            closeRecordingModal();
            recordingStatus.textContent = '';
        }, 2000);
    }
}

function toggleVideoRecording() {
    // Similar to audio recording but for video
    alert('Video recording feature would be implemented with WebRTC API');
}

function simulateRecording() {
    // Simulate recording duration counter
    let duration = 0;
    const recordingStatus = document.getElementById('recordingStatus');
    
    const interval = setInterval(() => {
        if (!isRecording) {
            clearInterval(interval);
            return;
        }
        
        duration++;
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        recordingStatus.textContent = `Recording... ${minutes}:${seconds.toString().padStart(2, '0')}`;
    }, 1000);
}

// Chart Generation
function generateMockChart() {
    const canvas = document.getElementById('progressChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Generate mock progress data
    const data = [];
    for (let i = 0; i < 12; i++) {
        data.push(Math.random() * 30 + 50 + (i * 2)); // Trending upward
    }
    
    // Draw chart
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 3;
    ctx.beginPath();
    
    const stepX = width / (data.length - 1);
    const maxY = Math.max(...data);
    const minY = Math.min(...data);
    const range = maxY - minY;
    
    data.forEach((point, index) => {
        const x = index * stepX;
        const y = height - ((point - minY) / range) * height;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
    
    // Add data points
    ctx.fillStyle = '#667eea';
    data.forEach((point, index) => {
        const x = index * stepX;
        const y = height - ((point - minY) / range) * height;
        
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fill();
    });
}

// AI Assessment Functions
function assessStudentPerformance(studentId, teacherComments) {
    // Simulate AI assessment based on teacher comments
    const assessment = {
        technical: Math.floor(Math.random() * 20 + 70),
        musicianship: Math.floor(Math.random() * 20 + 65),
        repertoire: Math.floor(Math.random() * 20 + 60),
        artistry: Math.floor(Math.random() * 20 + 75)
    };
    
    // Generate assignments based on weak areas
    const assignments = generateAssignments(assessment);
    
    return {
        assessment,
        assignments,
        overallScore: Math.round((assessment.technical + assessment.musicianship + assessment.repertoire + assessment.artistry) / 4)
    };
}

function generateAssignments(assessment) {
    const assignments = [];
    
    if (assessment.technical < 75) {
        assignments.push({
            title: "Technical Skills Improvement",
            description: "Practice scales and arpeggios daily for 15 minutes",
            category: "technical"
        });
    }
    
    if (assessment.musicianship < 70) {
        assignments.push({
            title: "Music Theory Study",
            description: "Complete harmony exercises and sight-reading practice",
            category: "musicianship"
        });
    }
    
    if (assessment.repertoire < 65) {
        assignments.push({
            title: "Repertoire Expansion",
            description: "Learn one new piece from a different musical period",
            category: "repertoire"
        });
    }
    
    if (assessment.artistry < 80) {
        assignments.push({
            title: "Performance Expression",
            description: "Record performance focusing on dynamics and phrasing",
            category: "artistry"
        });
    }
    
    return assignments;
}

// Alert System
function generateAlerts() {
    const alerts = [];
    
    // Check for struggling students
    mockStudents.forEach(student => {
        Object.entries(student.dimensions).forEach(([dimension, score]) => {
            if (score < 65) {
                alerts.push({
                    type: 'warning',
                    message: `${student.name} struggling with ${dimension} (${score}%) - recommend additional support`,
                    studentId: student.id,
                    category: dimension
                });
            }
        });
    });
    
    return alerts;
}

function addTeacherAlerts() {
    const alerts = generateAlerts();
    // Add alerts to teacher dashboard
    console.log('Teacher alerts:', alerts);
}

function addAdminMetrics() {
    // Add admin-specific metrics and teacher performance data
    console.log('Admin metrics updated');
}

// Utility Functions
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(date);
}

function calculateProgress(current, target) {
    return Math.min(100, Math.round((current / target) * 100));
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('recordingModal');
    if (event.target === modal) {
        closeRecordingModal();
    }
}

// Simulate real-time updates
setInterval(() => {
    // Update progress indicators
    const progressElements = document.querySelectorAll('.score-fill');
    progressElements.forEach(element => {
        const currentWidth = parseInt(element.style.width);
        if (Math.random() < 0.1) { // 10% chance to update
            const newWidth = Math.min(100, currentWidth + Math.floor(Math.random() * 3));
            element.style.width = newWidth + '%';
        }
    });
}, 30000); // Update every 30 seconds

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        assessStudentPerformance,
        generateAssignments,
        generateAlerts,
        mockStudents,
        mockAIFeedback
    };
}