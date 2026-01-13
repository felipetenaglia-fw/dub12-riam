// Admin Dashboard JavaScript
let currentPage = 'dashboard';
let adminData = {
    systemStats: {
        totalStudents: 1247,
        activeTeachers: 89,
        activeModules: 156,
        aiAssessments: 15432
    },
    platformHealth: {
        uptime: 99.8,
        aiResponseTime: 1.2,
        userSatisfaction: 4.6
    },
    teachers: [
        {
            id: 1,
            name: "Ms. Anderson",
            department: "Piano",
            experience: 15,
            students: 15,
            avgProgress: 12.5,
            satisfaction: 4.8,
            responseTime: 2.3,
            completionRate: 87,
            performance: "excellent"
        },
        {
            id: 2,
            name: "Mr. Thompson",
            department: "Violin",
            experience: 8,
            students: 12,
            avgProgress: 6.2,
            satisfaction: 3.8,
            responseTime: 5.1,
            completionRate: 72,
            performance: "needs-support"
        }
    ]
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeAdmin();
    setupEventListeners();
    createCharts();
    updateRealTimeData();
});

function initializeAdmin() {
    showPage('dashboard');
    updateSystemStats();
    updatePlatformHealth();
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

    // Real-time updates
    setInterval(updateRealTimeData, 30000); // Update every 30 seconds
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
        switch(pageId) {
            case 'system-overview':
                updateSystemOverview();
                break;
            case 'teachers':
                updateTeachersView();
                break;
            case 'students':
                updateStudentsAnalytics();
                break;
            case 'ai-insights':
                updateAIInsights();
                break;
        }
    }
}

function updateActiveNav(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

function updateSystemStats() {
    const statValues = document.querySelectorAll('.system-stats .stat-value');
    if (statValues.length >= 4) {
        statValues[0].textContent = adminData.systemStats.totalStudents.toLocaleString();
        statValues[1].textContent = adminData.systemStats.activeTeachers;
        statValues[2].textContent = adminData.systemStats.activeModules;
        statValues[3].textContent = adminData.systemStats.aiAssessments.toLocaleString();
    }
}

function updatePlatformHealth() {
    const healthValues = document.querySelectorAll('.platform-health .health-value');
    if (healthValues.length >= 3) {
        healthValues[0].textContent = `${adminData.platformHealth.uptime}%`;
        healthValues[1].textContent = `${adminData.platformHealth.aiResponseTime}s avg`;
        healthValues[2].textContent = `${adminData.platformHealth.userSatisfaction}/5`;
    }
}

function updateRealTimeData() {
    // Simulate real-time updates
    adminData.systemStats.aiAssessments += Math.floor(Math.random() * 10);
    adminData.systemStats.totalStudents += Math.floor(Math.random() * 3);
    
    updateSystemStats();
    
    // Update activity timeline
    addRecentActivity();
}

function addRecentActivity() {
    const activities = [
        { icon: 'fas fa-user-plus', text: 'New student registration', time: 'Just now' },
        { icon: 'fas fa-robot', text: 'AI processed 50 new assessments', time: '2 min ago' },
        { icon: 'fas fa-exclamation-triangle', text: 'Performance alert triggered', time: '5 min ago' }
    ];
    
    const timeline = document.querySelector('.activity-timeline');
    if (timeline && Math.random() < 0.3) { // 30% chance to add new activity
        const randomActivity = activities[Math.floor(Math.random() * activities.length)];
        const activityElement = document.createElement('div');
        activityElement.className = 'activity-item';
        activityElement.innerHTML = `
            <i class="${randomActivity.icon}"></i>
            <div>
                <span>${randomActivity.text}</span>
                <small>${randomActivity.time}</small>
            </div>
        `;
        
        timeline.insertBefore(activityElement, timeline.firstChild);
        
        // Keep only last 5 activities
        while (timeline.children.length > 5) {
            timeline.removeChild(timeline.lastChild);
        }
    }
}

function createCharts() {
    createEngagementChart();
    createProgressRateChart();
    createAIAccuracyChart();
    createUsageTrendsChart();
    createPerformanceDistChart();
    createModulePopularityChart();
    createGradePerformanceChart();
    createImprovementTrendsChart();
    createEnrollmentTrendsChart();
    createAIAccuracyTrendChart();
    createInterventionOutcomesChart();
}

function createEngagementChart() {
    const canvas = document.getElementById('engagementChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                data: [82, 85, 87, 87],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { 
                x: { display: false },
                y: { display: false }
            }
        }
    });
}

function createProgressRateChart() {
    const canvas = document.getElementById('progressRateChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                data: [12.1, 13.5, 14.2, 14.2],
                backgroundColor: '#38a169',
                borderRadius: 2
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { 
                x: { display: false },
                y: { display: false }
            }
        }
    });
}

function createAIAccuracyChart() {
    const canvas = document.getElementById('aiAccuracyChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [94.3, 5.7],
                backgroundColor: ['#667eea', '#e2e8f0'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            cutout: '70%'
        }
    });
}

function createUsageTrendsChart() {
    const canvas = document.getElementById('usageTrendsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Active Students',
                data: [980, 1020, 1100, 1150, 1180, 1200, 1220, 1240, 1247, 1250, 1245, 1247],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'AI Assessments (hundreds)',
                data: [120, 125, 135, 140, 145, 148, 150, 152, 154, 155, 154, 154],
                borderColor: '#38b2ac',
                backgroundColor: 'rgba(56, 178, 172, 0.1)',
                tension: 0.4,
                fill: true
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
                    beginAtZero: false
                }
            }
        }
    });
}

function createPerformanceDistChart() {
    const canvas = document.getElementById('performanceDistChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Excellent (80%+)', 'Good (70-79%)', 'Satisfactory (60-69%)', 'Needs Support (<60%)'],
            datasets: [{
                data: [312, 456, 389, 90],
                backgroundColor: ['#38a169', '#667eea', '#ed8936', '#e53e3e'],
                borderWidth: 2,
                borderColor: '#fff'
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

function createModulePopularityChart() {
    const canvas = document.getElementById('modulePopularityChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Piano', 'Violin', 'Flute', 'Cello', 'Guitar', 'Voice'],
            datasets: [{
                label: 'Enrolled Students',
                data: [456, 321, 189, 156, 125, 98],
                backgroundColor: ['#667eea', '#38b2ac', '#ed8936', '#e53e3e', '#9f7aea', '#38a169'],
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
                    beginAtZero: true
                }
            }
        }
    });
}

function createGradePerformanceChart() {
    const canvas = document.getElementById('gradePerformanceChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8'],
            datasets: [{
                label: 'Average Performance',
                data: [85, 82, 78, 75, 73, 76, 79, 81],
                backgroundColor: '#667eea',
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
                    min: 60,
                    max: 90
                }
            }
        }
    });
}

function createImprovementTrendsChart() {
    const canvas = document.getElementById('improvementTrendsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
            datasets: [{
                label: 'Technical Skills',
                data: [8.2, 9.1, 10.5, 11.8, 12.3],
                borderColor: '#667eea',
                tension: 0.4
            }, {
                label: 'Musicianship',
                data: [7.5, 8.2, 9.0, 10.1, 11.2],
                borderColor: '#38b2ac',
                tension: 0.4
            }, {
                label: 'Artistry',
                data: [9.1, 10.2, 11.5, 12.8, 14.1],
                borderColor: '#e53e3e',
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
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Improvement Rate (%)'
                    }
                }
            }
        }
    });
}

function createEnrollmentTrendsChart() {
    const canvas = document.getElementById('enrollmentTrendsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'New Enrollments',
                data: [45, 52, 48, 61, 55, 67, 72, 68, 58, 63, 59, 61],
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
                    beginAtZero: true
                }
            }
        }
    });
}

function createAIAccuracyTrendChart() {
    const canvas = document.getElementById('aiAccuracyTrendChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
            datasets: [{
                label: 'Prediction Accuracy',
                data: [91.2, 92.1, 92.8, 93.2, 93.5, 93.8, 94.1, 94.3],
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
                    min: 90,
                    max: 95
                }
            }
        }
    });
}

function createInterventionOutcomesChart() {
    const canvas = document.getElementById('interventionOutcomesChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Successful', 'Partially Successful', 'Needs Follow-up'],
            datasets: [{
                data: [87, 10, 3],
                backgroundColor: ['#38a169', '#ed8936', '#e53e3e'],
                borderWidth: 2,
                borderColor: '#fff'
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

// Page-specific update functions
function updateSystemOverview() {
    // Update engagement, progress rate, and AI accuracy metrics
    const metricValues = document.querySelectorAll('.metrics-overview .metric-value');
    if (metricValues.length >= 3) {
        metricValues[0].textContent = '87%';
        metricValues[1].textContent = '+14.2%';
        metricValues[2].textContent = '94.3%';
    }
}

function updateTeachersView() {
    // This would update the teachers grid with current data
    console.log('Updating teachers view with current performance data');
}

function updateStudentsAnalytics() {
    // Update student analytics metrics
    const metricValues = document.querySelectorAll('.students-analytics-container .metric-value');
    if (metricValues.length >= 3) {
        metricValues[0].textContent = adminData.systemStats.totalStudents.toLocaleString();
        metricValues[1].textContent = '76.3%';
        metricValues[2].textContent = '89';
    }
}

function updateAIInsights() {
    // Update AI performance metrics
    const metricValues = document.querySelectorAll('.ai-performance-metrics .metric-value');
    if (metricValues.length >= 3) {
        metricValues[0].textContent = '94.3%';
        metricValues[1].textContent = adminData.systemStats.aiAssessments.toLocaleString();
        metricValues[2].textContent = '87%';
    }
}

// Teacher Management Functions
function addTeacher() {
    showTeacherModal();
}

function viewTeacher(teacherId) {
    const teacher = adminData.teachers.find(t => t.id === teacherId);
    if (teacher) {
        showTeacherDetailsModal(teacher);
    }
}

function messageTeacher(teacherId) {
    showNotification(`Opening message interface for teacher ${teacherId}`);
}

function supportTeacher(teacherId) {
    showSupportModal(teacherId);
}

function showTeacherModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Add New Teacher</h3>
                <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
            </div>
            <div class="modal-body">
                <form id="teacherForm">
                    <div class="form-group">
                        <label>Full Name</label>
                        <input type="text" required>
                    </div>
                    <div class="form-group">
                        <label>Department</label>
                        <select required>
                            <option>Piano</option>
                            <option>Strings</option>
                            <option>Woodwinds</option>
                            <option>Brass</option>
                            <option>Voice</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Experience (years)</label>
                        <input type="number" min="0" required>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" required>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn-primary">Add Teacher</button>
                        <button type="button" class="btn-outline" onclick="this.closest('.modal').remove()">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    modal.querySelector('#teacherForm').addEventListener('submit', function(e) {
        e.preventDefault();
        showNotification('Teacher added successfully!');
        modal.remove();
    });
}

function showTeacherDetailsModal(teacher) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content large">
            <div class="modal-header">
                <h3>${teacher.name} - Performance Details</h3>
                <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
            </div>
            <div class="modal-body">
                <div class="teacher-performance-details">
                    <div class="performance-section">
                        <h4>Teaching Metrics</h4>
                        <div class="metrics-grid">
                            <div class="metric-item">
                                <span>Students</span>
                                <span>${teacher.students}</span>
                            </div>
                            <div class="metric-item">
                                <span>Avg Student Progress</span>
                                <span class="${teacher.avgProgress > 10 ? 'positive' : 'negative'}">+${teacher.avgProgress}%</span>
                            </div>
                            <div class="metric-item">
                                <span>Student Satisfaction</span>
                                <span>${teacher.satisfaction}/5</span>
                            </div>
                            <div class="metric-item">
                                <span>Response Time</span>
                                <span>${teacher.responseTime}h</span>
                            </div>
                            <div class="metric-item">
                                <span>Assignment Completion</span>
                                <span>${teacher.completionRate}%</span>
                            </div>
                        </div>
                    </div>
                    ${teacher.performance === 'needs-support' ? `
                        <div class="support-section">
                            <h4>Support Recommendations</h4>
                            <ul>
                                <li>Professional development in modern teaching techniques</li>
                                <li>Mentorship program with high-performing teachers</li>
                                <li>Additional training in student engagement strategies</li>
                            </ul>
                            <button class="btn-primary" onclick="scheduleSupport(${teacher.id})">Schedule Support</button>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

function showSupportModal(teacherId) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Provide Teacher Support</h3>
                <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
            </div>
            <div class="modal-body">
                <div class="support-options">
                    <h4>Available Support Options</h4>
                    <div class="support-list">
                        <label class="support-option">
                            <input type="checkbox" checked>
                            <span>Professional Development Workshop</span>
                        </label>
                        <label class="support-option">
                            <input type="checkbox">
                            <span>Peer Mentorship Program</span>
                        </label>
                        <label class="support-option">
                            <input type="checkbox">
                            <span>Teaching Technique Training</span>
                        </label>
                        <label class="support-option">
                            <input type="checkbox">
                            <span>One-on-One Coaching</span>
                        </label>
                    </div>
                    <div class="form-group">
                        <label>Additional Notes</label>
                        <textarea placeholder="Specific areas of focus or concerns..."></textarea>
                    </div>
                    <div class="form-actions">
                        <button class="btn-primary" onclick="scheduleSupport(${teacherId})">Schedule Support</button>
                        <button class="btn-outline" onclick="this.closest('.modal').remove()">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

function scheduleSupport(teacherId) {
    showNotification('Support scheduled successfully! Teacher will be notified.');
    document.querySelector('.modal').remove();
}

// Module Management Functions
function createModule() {
    showNotification('Opening module creation interface...');
}

// Report Generation Functions
function generateReport() {
    showNotification('Generating comprehensive system report...');
    
    // Simulate report generation
    setTimeout(() => {
        showNotification('Report generated successfully! Check your downloads.');
    }, 3000);
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

// Add CSS for admin-specific styles
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
    
    .modal-content.large {
        max-width: 800px;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    
    .metric-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        background: #f7fafc;
        border-radius: 4px;
    }
    
    .positive {
        color: #38a169;
        font-weight: bold;
    }
    
    .negative {
        color: #e53e3e;
        font-weight: bold;
    }
    
    .support-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .support-option {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .support-option:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }
    
    .support-option input[type="checkbox"] {
        margin: 0;
    }
`;
document.head.appendChild(style);