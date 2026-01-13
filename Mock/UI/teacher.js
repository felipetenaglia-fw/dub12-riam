// Teacher Dashboard JavaScript
let currentPage = 'dashboard';
let teacherData = {
    name: "Ms. Anderson",
    department: "Piano",
    students: [
        {
            id: 1,
            name: "Emma Johnson",
            module: "Advanced Piano Performance",
            overallScore: 78,
            status: "active",
            lastSeen: "2h ago",
            dimensions: { technical: 82, musicianship: 75, repertoire: 70, artistry: 85 },
            needsAttention: false
        },
        {
            id: 2,
            name: "James Wilson",
            module: "Intermediate Violin",
            overallScore: 65,
            status: "needs-attention",
            lastSeen: "1d ago",
            dimensions: { technical: 60, musicianship: 68, repertoire: 62, artistry: 70 },
            needsAttention: true
        }
    ]
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeTeacher();
    setupEventListeners();
    createCharts();
});

function initializeTeacher() {
    showPage('dashboard');
    updateDashboardStats();
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

    // Assignment tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterAssignmentsByTab(this.getAttribute('data-tab'));
        });
    });

    // Assignment form
    const assignmentForm = document.getElementById('assignmentForm');
    if (assignmentForm) {
        assignmentForm.addEventListener('submit', handleAssignmentSubmit);
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
        
        // Load page-specific data
        if (pageId === 'analytics') {
            updateAnalytics();
        } else if (pageId === 'submissions') {
            loadSubmissions();
        }
    }
}

function updateActiveNav(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

function updateDashboardStats() {
    // Update overview stats
    const totalStudents = teacherData.students.length;
    const needsAttention = teacherData.students.filter(s => s.needsAttention).length;
    const pendingReviews = 23; // Mock data
    
    const statValues = document.querySelectorAll('.overview-stats .stat-value');
    if (statValues.length >= 3) {
        statValues[0].textContent = totalStudents;
        statValues[1].textContent = pendingReviews;
        statValues[2].textContent = needsAttention;
    }
}

function createCharts() {
    createClassPerformanceChart();
    createModuleProgressChart();
    createProgressDistributionChart();
    createAssignmentTrendsChart();
}

function createClassPerformanceChart() {
    const canvas = document.getElementById('classPerformanceChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
            datasets: [{
                label: 'Class Average',
                data: [68, 71, 74, 76, 78],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 60,
                    max: 90
                }
            }
        }
    });
}

function createModuleProgressChart() {
    const canvas = document.getElementById('moduleProgressChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Excellent (80%+)', 'Good (70-79%)', 'Needs Work (<70%)'],
            datasets: [{
                data: [3, 4, 1],
                backgroundColor: ['#38a169', '#ed8936', '#e53e3e'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createProgressDistributionChart() {
    const canvas = document.getElementById('progressDistributionChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Technical Skills', 'Musicianship', 'Repertoire', 'Artistry'],
            datasets: [{
                label: 'Class Average',
                data: [71, 71.5, 66, 77.5],
                backgroundColor: ['#667eea', '#38b2ac', '#ed8936', '#e53e3e'],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
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

function createAssignmentTrendsChart() {
    const canvas = document.getElementById('assignmentTrendsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Completion Rate',
                data: [85, 78, 92, 87],
                borderColor: '#38a169',
                backgroundColor: 'rgba(56, 161, 105, 0.1)',
                tension: 0.4
            }, {
                label: 'Average Score',
                data: [76, 74, 81, 78],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
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
                    min: 60,
                    max: 100
                }
            }
        }
    });
}

// Student Management Functions
function viewStudent(studentId) {
    const student = teacherData.students.find(s => s.id === studentId);
    if (student) {
        showStudentModal(student);
    }
}

function messageStudent(studentId) {
    showNotification(`Opening chat with student ${studentId}`);
    // This would open a messaging interface
}

function showStudentModal(student) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>${student.name} - Detailed View</h3>
                <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
            </div>
            <div class="modal-body">
                <div class="student-details">
                    <div class="detail-section">
                        <h4>Performance Metrics</h4>
                        <div class="metrics-grid">
                            <div class="metric-item">
                                <span>Technical Skills</span>
                                <div class="metric-bar">
                                    <div class="metric-fill" style="width: ${student.dimensions.technical}%"></div>
                                </div>
                                <span>${student.dimensions.technical}%</span>
                            </div>
                            <div class="metric-item">
                                <span>Musicianship</span>
                                <div class="metric-bar">
                                    <div class="metric-fill" style="width: ${student.dimensions.musicianship}%"></div>
                                </div>
                                <span>${student.dimensions.musicianship}%</span>
                            </div>
                            <div class="metric-item">
                                <span>Repertoire</span>
                                <div class="metric-bar">
                                    <div class="metric-fill" style="width: ${student.dimensions.repertoire}%"></div>
                                </div>
                                <span>${student.dimensions.repertoire}%</span>
                            </div>
                            <div class="metric-item">
                                <span>Artistry</span>
                                <div class="metric-bar">
                                    <div class="metric-fill" style="width: ${student.dimensions.artistry}%"></div>
                                </div>
                                <span>${student.dimensions.artistry}%</span>
                            </div>
                        </div>
                    </div>
                    <div class="detail-section">
                        <h4>Recent Activity</h4>
                        <p>Last submission: Bach Invention Performance</p>
                        <p>Practice time this week: 8.5 hours</p>
                        <p>Assignment completion rate: 85%</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

// Assignment Management Functions
function createAssignment() {
    const modal = document.getElementById('assignmentModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeAssignmentModal() {
    const modal = document.getElementById('assignmentModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function handleAssignmentSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const assignmentData = {
        title: formData.get('title'),
        description: formData.get('description'),
        dueDate: formData.get('dueDate'),
        points: formData.get('points'),
        students: Array.from(e.target.querySelectorAll('select[multiple] option:checked')).map(opt => opt.value)
    };
    
    // Simulate assignment creation
    showNotification('Assignment created successfully!');
    closeAssignmentModal();
    
    // Add to assignments list
    addAssignmentToList(assignmentData);
}

function addAssignmentToList(assignmentData) {
    const assignmentsList = document.querySelector('.assignments-list');
    const newAssignment = document.createElement('div');
    newAssignment.className = 'assignment-item';
    newAssignment.innerHTML = `
        <div class="assignment-info">
            <h3>${assignmentData.title}</h3>
            <p>${assignmentData.description}</p>
            <div class="assignment-meta">
                <span><i class="fas fa-users"></i> ${assignmentData.students.length} students</span>
                <span><i class="fas fa-calendar"></i> Due: ${assignmentData.dueDate}</span>
                <span><i class="fas fa-star"></i> ${assignmentData.points} points</span>
            </div>
        </div>
        <div class="assignment-progress">
            <div class="progress-stats">
                <span>0/${assignmentData.students.length} submitted</span>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
            </div>
        </div>
        <div class="assignment-actions">
            <button class="btn-outline">View Submissions</button>
            <button class="btn-outline">Edit</button>
        </div>
    `;
    
    assignmentsList.prepend(newAssignment);
}

function filterAssignmentsByTab(tab) {
    // This would filter assignments based on the selected tab
    showNotification(`Showing ${tab} assignments`);
}

// Submission Management Functions
function loadSubmissions() {
    // This would load and display student submissions
    console.log('Loading submissions for review');
}

function gradeSubmission(submissionId, grade, feedback) {
    // Simulate grading
    showNotification('Grade submitted successfully!');
    
    // Update UI to show graded status
    const submissionCard = document.querySelector(`[data-submission-id="${submissionId}"]`);
    if (submissionCard) {
        submissionCard.classList.remove('pending');
        submissionCard.classList.add('graded');
        
        const statusElement = submissionCard.querySelector('.submission-status');
        if (statusElement) {
            statusElement.textContent = `Graded: ${grade}/100`;
            statusElement.className = 'submission-status graded';
        }
    }
}

// Analytics Functions
function updateAnalytics() {
    // Update teaching analytics with current data
    const avgImprovement = teacherData.students.reduce((sum, student) => sum + (student.overallScore - 65), 0) / teacherData.students.length;
    const completionRate = 87; // Mock data
    const satisfaction = 4.8; // Mock data
    
    const metricValues = document.querySelectorAll('.analytics-overview .metric-value');
    if (metricValues.length >= 3) {
        metricValues[0].textContent = `+${avgImprovement.toFixed(1)}%`;
        metricValues[1].textContent = `${completionRate}%`;
        metricValues[2].textContent = `${satisfaction}/5`;
    }
}

// AI Assistant Functions
function sendTeacherAIMessage() {
    const input = document.getElementById('teacherAIInput');
    const chatMessages = document.getElementById('teacherAIChat');
    
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
        const aiResponse = generateTeacherAIResponse(userInput);
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

function generateTeacherAIResponse(userInput) {
    const input = userInput.toLowerCase();
    
    if (input.includes('james') || input.includes('struggling')) {
        return "James Wilson is indeed showing some challenges. His technical skills are at 60%, which is below the class average of 71%. I recommend creating targeted bow technique exercises and scheduling additional one-on-one time. His musicianship knowledge is actually quite good at 68%, so focus on the technical foundation.";
    } else if (input.includes('emma') || input.includes('advanced')) {
        return "Emma Johnson is performing excellently with 78% overall! Her artistry score of 85% is outstanding. She's ready for more challenging repertoire. Consider introducing Grade 7 pieces or competition preparation. Her weakest area is repertoire knowledge at 70% - perhaps explore different musical periods.";
    } else if (input.includes('assignment') || input.includes('create')) {
        return "Based on your class performance data, I suggest creating assignments focused on technical skills, as this is where most students need improvement (class average: 71%). Consider bow technique exercises for string students or pedaling exercises for piano students. Would you like me to generate specific assignment ideas?";
    } else if (input.includes('class') || input.includes('overall')) {
        return "Your class is performing well with an average improvement of +12.5% this semester! The strongest area is Performance Artistry (77.5% average) and the area needing most attention is Repertoire Knowledge (66% average). Consider incorporating more music history and style analysis into your lessons.";
    } else if (input.includes('feedback') || input.includes('grading')) {
        return "Your average response time of 2.3 hours is excellent! Students respond well to timely feedback. I notice your feedback often focuses on technical aspects - consider adding more comments about musical expression and interpretation to help students develop their artistry further.";
    } else {
        return "I'm here to help with your teaching! I can analyze student performance data, suggest assignments, help with grading strategies, or provide insights about individual students. Your teaching effectiveness is strong with 87% assignment completion rate and 4.8/5 student satisfaction. What specific area would you like to discuss?";
    }
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

// Close modals when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Add CSS for teacher-specific styles
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
    
    .metrics-grid {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .metric-item {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .metric-item span:first-child {
        min-width: 120px;
        font-size: 0.9rem;
    }
    
    .metric-bar {
        flex: 1;
        height: 8px;
        background: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .metric-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.8s ease;
    }
    
    .metric-item span:last-child {
        min-width: 40px;
        text-align: right;
        font-weight: bold;
        color: #2d3748;
    }
`;
document.head.appendChild(style);