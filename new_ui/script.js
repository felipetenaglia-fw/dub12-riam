// API Configuration
const API_CONFIG = {
    baseURL: 'http://localhost:8000',
    endpoints: {
        aiCoach: '/ai-coach/analyze',  // Using authenticated endpoint
        login: '/auth/login',
        me: '/auth/me'
    }
};

// Authentication state
let authToken = localStorage.getItem('access_token');
let currentUser = JSON.parse(localStorage.getItem('user') || 'null');

// Check authentication on page load
function checkAuth() {
    if (!authToken || !currentUser) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Get auth headers for API calls
function getAuthHeaders() {
    return {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
    };
}

// Function to logout
function performLogout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// Update UI with user information
function updateUIWithUser() {
    if (currentUser) {
        // Update welcome message
        const welcomeElements = document.querySelectorAll('.dashboard-header h1');
        welcomeElements.forEach(el => {
            if (el.textContent.includes('Welcome') || el.textContent.includes('Good morning')) {
                el.textContent = `Welcome back, ${currentUser.name || currentUser.username}!`;
            }
        });
        
        // Update student name in passport
        const passportName = document.querySelector('.passport-info h2');
        if (passportName) {
            passportName.textContent = currentUser.name || currentUser.username;
        }
        
        // Update persona button if user is teacher
        const personaBtn = document.getElementById('personaBtn');
        const personaText = document.getElementById('personaText');
        if (currentUser.role === 'teacher') {
            if (personaBtn && personaText) {
                personaText.textContent = 'Teacher';
                personaBtn.innerHTML = '<i class="fas fa-chalkboard-teacher"></i><span id="personaText">Teacher</span>';
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Check authentication first
    if (!checkAuth()) {
        return;
    }
    
    // Update UI with user info
    updateUIWithUser();
    
    const personaBtn = document.getElementById('personaBtn');
    const personaText = document.getElementById('personaText');
    const studentDashboard = document.getElementById('studentDashboard');
    const teacherDashboard = document.getElementById('teacherDashboard');
    const sessionDetails = document.getElementById('sessionDetails');
    
    let isStudent = true;
    
    personaBtn.addEventListener('click', function() {
        // Add click animation
        personaBtn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            personaBtn.style.transform = '';
        }, 150);
        
        // Toggle persona
        isStudent = !isStudent;
        
        // Hide all pages first
        hideAllPages();
        
        if (isStudent) {
            // Switch to student
            personaText.textContent = 'Student';
            personaBtn.innerHTML = '<i class="fas fa-user-graduate"></i><span id="personaText">Student</span>';
            document.body.style.background = 'linear-gradient(135deg, #00B1D3 0%, #8874B3 100%)';
            document.body.style.backgroundAttachment = 'fixed';
            
            setTimeout(() => {
                studentDashboard.classList.add('active');
            }, 250);
            
        } else {
            // Switch to teacher
            personaText.textContent = 'Teacher';
            personaBtn.innerHTML = '<i class="fas fa-chalkboard-teacher"></i><span id="personaText">Teacher</span>';
            document.body.style.background = 'linear-gradient(135deg, #231F20 0%, #00B1D3 100%)';
            document.body.style.backgroundAttachment = 'fixed';
            
            setTimeout(() => {
                teacherDashboard.classList.add('active');
            }, 250);
        }
        
        // Re-assign the personaText element after innerHTML change
        setTimeout(() => {
            const newPersonaText = document.getElementById('personaText');
            if (newPersonaText) {
                newPersonaText.textContent = isStudent ? 'Student' : 'Teacher';
            }
        }, 10);
    });
    
    // Add hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add click effects to action buttons
    const actionBtns = document.querySelectorAll('.action-btn');
    actionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Create ripple effect
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.left = '50%';
            ripple.style.top = '50%';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.marginLeft = '-10px';
            ripple.style.marginTop = '-10px';
            
            this.style.position = 'relative';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Animate progress bars on load
    setTimeout(() => {
        const progressFills = document.querySelectorAll('.progress-fill');
        progressFills.forEach(fill => {
            const width = fill.style.width;
            fill.style.width = '0';
            setTimeout(() => {
                fill.style.width = width;
            }, 100);
        });
    }, 1000);
    
    // Add floating animation to logo
    const logo = document.querySelector('.logo img');
    if (logo) {
        setInterval(() => {
            logo.style.transform = 'translateY(-2px)';
            setTimeout(() => {
                logo.style.transform = 'translateY(0)';
            }, 1000);
        }, 3000);
    }
});

// Helper function to hide all pages
function hideAllPages() {
    const allPages = ['studentDashboard', 'teacherDashboard', 'sessionDetails', 'assignmentDetails', 'aiAnalysis', 'classReport', 'progressHistory', 'aiCoachPage'];
    allPages.forEach(pageId => {
        const page = document.getElementById(pageId);
        if (page) {
            page.classList.remove('active');
            if (page.classList.contains('session-page')) {
                page.style.display = 'none';
            }
        }
    });
}

// Home function for logo click
function goToHome() {
    hideAllPages();
    const isStudent = document.getElementById('personaText').textContent === 'Student';
    if (isStudent) {
        setTimeout(() => {
            document.getElementById('studentDashboard').classList.add('active');
        }, 250);
    } else {
        setTimeout(() => {
            document.getElementById('teacherDashboard').classList.add('active');
        }, 250);
    }
}

// Add CSS for ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Session Details Functions
function openSessionDetails() {
    const teacherDashboard = document.getElementById('teacherDashboard');
    const sessionDetails = document.getElementById('sessionDetails');
    
    teacherDashboard.classList.remove('active');
    sessionDetails.style.display = 'block';
    setTimeout(() => {
        sessionDetails.classList.add('active');
    }, 50);
}

function closeSessionDetails() {
    const teacherDashboard = document.getElementById('teacherDashboard');
    const sessionDetails = document.getElementById('sessionDetails');
    
    sessionDetails.classList.remove('active');
    setTimeout(() => {
        sessionDetails.style.display = 'none';
        teacherDashboard.classList.add('active');
    }, 250);
}

function processNotes() {
    const processBtn = document.getElementById('processNotesBtn');
    const processingAnimation = document.getElementById('processingAnimation');
    const tasksCard = document.getElementById('tasksCard');
    
    // Hide button and show processing animation
    processBtn.style.display = 'none';
    processingAnimation.style.display = 'block';
    
    // After 2 seconds, hide animation and show tasks
    setTimeout(() => {
        processingAnimation.style.display = 'none';
        tasksCard.style.display = 'block';
        tasksCard.style.animation = 'fadeInUp 0.5s ease-out';
    }, 2000);
}

function approveAndAssign() {
    const tasksCard = document.getElementById('tasksCard');
    const successMessage = document.getElementById('successMessage');
    
    // Hide tasks card and show success message
    tasksCard.style.display = 'none';
    successMessage.style.display = 'block';
}

// Assignment Functions
let uploadedFiles = { pdf: false, audio: false };
let uploadedAudioFile = null;

console.log('Script loaded! Assignment functions initialized.');

function openAssignmentDetails() {
    console.log('Opening assignment details...');
    const studentDashboard = document.getElementById('studentDashboard');
    const assignmentDetails = document.getElementById('assignmentDetails');
    
    studentDashboard.classList.remove('active');
    assignmentDetails.style.display = 'block';
    setTimeout(() => {
        assignmentDetails.classList.add('active');
    }, 50);
}

function closeAssignmentDetails() {
    const studentDashboard = document.getElementById('studentDashboard');
    const assignmentDetails = document.getElementById('assignmentDetails');
    
    assignmentDetails.classList.remove('active');
    setTimeout(() => {
        assignmentDetails.style.display = 'none';
        studentDashboard.classList.add('active');
    }, 250);
}

function handleFileUpload(type) {
    console.log('handleFileUpload called with type:', type);
    
    const statusElement = document.getElementById(type + 'Status');
    const inputElement = document.getElementById(type + 'Upload');
    
    if (!inputElement) {
        console.error('Input element not found for type:', type);
        return;
    }
    
    // Get the uploaded file
    const file = inputElement.files[0];
    
    console.log('File selected:', file ? file.name : 'none');
    
    if (file) {
        // For audio files, open AI Coach page instead of just showing status
        if (type === 'audio') {
            uploadedAudioFile = file;
            console.log('Audio file stored, opening AI Coach...', file.name, file.size, 'bytes');
            openAICoachWithFile(file);
            return; // Exit early - don't need submit button logic
        }
        
        // For PDF, just show status
        if (statusElement) {
            statusElement.innerHTML = `<i class="fas fa-check-circle"></i> File uploaded: ${file.name}`;
            statusElement.style.color = '#28a745';
        }
        
        uploadedFiles[type] = true;
        console.log('Upload status:', uploadedFiles);
    } else {
        console.warn('No file selected');
    }
}

// AI Coach dedicated page functions
function openAICoachWithFile(audioFile) {
    console.log('Opening AI Coach page with file:', audioFile.name);
    
    const assignmentDetails = document.getElementById('assignmentDetails');
    const aiCoachPage = document.getElementById('aiCoachPage');
    
    // Hide assignment details
    if (assignmentDetails) {
        assignmentDetails.classList.remove('active');
        assignmentDetails.style.display = 'none';
    }
    
    // Store the file globally
    uploadedAudioFile = audioFile;
    
    // Update the filename display
    const audioNameSpan = document.getElementById('aiCoachAudioName');
    if (audioNameSpan) {
        audioNameSpan.textContent = `✓ ${audioFile.name}`;
        audioNameSpan.style.color = '#28a745';
        audioNameSpan.style.fontWeight = '600';
    }
    
    // Show AI Coach page
    if (aiCoachPage) {
        aiCoachPage.style.display = 'block';
        setTimeout(() => {
            aiCoachPage.classList.add('active');
        }, 50);
    }
}

function handleAICoachAudioSelect() {
    const input = document.getElementById('aiCoachAudioInput');
    const file = input.files[0];
    
    if (file) {
        uploadedAudioFile = file;
        const audioNameSpan = document.getElementById('aiCoachAudioName');
        if (audioNameSpan) {
            audioNameSpan.textContent = `✓ ${file.name}`;
            audioNameSpan.style.color = '#28a745';
            audioNameSpan.style.fontWeight = '600';
        }
        console.log('AI Coach audio selected:', file.name);
    }
}

function closeAICoach() {
    const assignmentDetails = document.getElementById('assignmentDetails');
    const aiCoachPage = document.getElementById('aiCoachPage');
    
    if (aiCoachPage) {
        aiCoachPage.classList.remove('active');
        setTimeout(() => {
            aiCoachPage.style.display = 'none';
            
            // Reset form
            document.getElementById('aiCoachPieceName').value = '';
            document.getElementById('aiCoachComposer').value = '';
            document.getElementById('aiCoachNotes').value = '';
            document.getElementById('aiCoachAudioName').textContent = '';
            
            // Show form, hide results
            document.getElementById('aiCoachForm').style.display = 'block';
            document.getElementById('aiCoachLoading').style.display = 'none';
            document.getElementById('aiCoachResults').style.display = 'none';
            
            // Return to assignment details
            if (assignmentDetails) {
                assignmentDetails.style.display = 'block';
                setTimeout(() => {
                    assignmentDetails.classList.add('active');
                }, 50);
            }
        }, 250);
    }
}

async function startAICoachAnalysis() {
    if (!uploadedAudioFile) {
        alert('Please select an audio file first!');
        return;
    }
    
    console.log('Starting AI Coach analysis...');
    
    // Get context from form
    const pieceName = document.getElementById('aiCoachPieceName').value.trim();
    const composer = document.getElementById('aiCoachComposer').value.trim();
    const notes = document.getElementById('aiCoachNotes').value.trim();
    
    // Hide form, show loading
    document.getElementById('aiCoachForm').style.display = 'none';
    document.getElementById('aiCoachLoading').style.display = 'block';
    
    try {
        const result = await analyzeAudioWithAI(uploadedAudioFile, {
            piece_name: pieceName || undefined,
            composer: composer || undefined,
            student_notes: notes || undefined
        });
        
        console.log('Analysis complete:', result);
        
        if (result.success) {
            displayAICoachResultsInPage(result);
            
            // Hide loading, show results
            document.getElementById('aiCoachLoading').style.display = 'none';
            document.getElementById('aiCoachResults').style.display = 'block';
        } else {
            throw new Error(result.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Error analyzing audio:', error);
        alert('AI analysis encountered an error: ' + error.message);
        
        // Return to form
        document.getElementById('aiCoachLoading').style.display = 'none';
        document.getElementById('aiCoachForm').style.display = 'block';
    }
}

function displayAICoachResultsInPage(analysisResult) {
    currentAIAnalysis = analysisResult;
    
    const analysis = analysisResult.audio_analysis;
    if (!analysis) {
        console.error('No audio analysis data found');
        return;
    }
    
    const scores = analysis.performance_scores;
    
    // Calculate Four Pillars scores
    const technicalSkills = Math.round(scores.technical_proficiency * 100);
    const performingArtistry = Math.round(scores.expressiveness * 100);
    const compositional = Math.round((
        analysis.pitch_intonation.pitch_stability_score * 100 +
        analysis.musical_structure.musical_development_score * 100
    ) / 2);
    const repertoire = Math.round((
        analysis.dynamics.dynamic_contrast_score * 100 +
        analysis.tone_quality.brightness_consistency * 100
    ) / 2);
    const overall = Math.round(scores.overall_score * 100);
    
    // Display scores with detailed metrics
    const scoresContainer = document.getElementById('aiCoachScores');
    scoresContainer.innerHTML = `
        <!-- Overall Scores Summary -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem;">
            <div style="text-align: center; padding: 1.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 12px;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #667eea; margin-bottom: 0.25rem;">${overall}</div>
                <div style="font-size: 0.9rem; color: #666;">Overall Score</div>
            </div>
            <div style="text-align: center; padding: 1.5rem; background: rgba(40, 167, 69, 0.1); border-radius: 12px;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #28a745; margin-bottom: 0.25rem;">${technicalSkills}</div>
                <div style="font-size: 0.9rem; color: #666;">Technical</div>
            </div>
            <div style="text-align: center; padding: 1.5rem; background: rgba(118, 75, 162, 0.1); border-radius: 12px;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #764ba2; margin-bottom: 0.25rem;">${performingArtistry}</div>
                <div style="font-size: 0.9rem; color: #666;">Expression</div>
            </div>
        </div>

        <!-- Detailed Metrics Grid -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; margin-bottom: 1.5rem;">
            <!-- Tempo -->
            <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">Tempo</div>
                <div style="font-weight: 600; font-size: 1rem;">${Math.round(analysis.tempo_rhythm.tempo_bpm)} BPM</div>
                <div style="font-size: 0.75rem; color: #999;">${analysis.tempo_rhythm.tempo_category}</div>
            </div>
            
            <!-- Tempo Stability -->
            <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">Tempo Stability</div>
                <div style="font-weight: 600; font-size: 1rem;">${Math.round(analysis.tempo_rhythm.tempo_stability_score * 100)}%</div>
                <div style="width: 100%; height: 4px; background: #e0e0e0; border-radius: 2px; margin-top: 0.25rem;">
                    <div style="width: ${analysis.tempo_rhythm.tempo_stability_score * 100}%; height: 100%; background: #667eea; border-radius: 2px;"></div>
                </div>
            </div>
            
            <!-- Key -->
            <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">Key</div>
                <div style="font-weight: 600; font-size: 1rem;">${analysis.pitch_intonation.estimated_key}</div>
            </div>
            
            <!-- Pitch Stability -->
            <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">Pitch Stability</div>
                <div style="font-weight: 600; font-size: 1rem;">${Math.round(analysis.pitch_intonation.pitch_stability_score * 100)}%</div>
                <div style="width: 100%; height: 4px; background: #e0e0e0; border-radius: 2px; margin-top: 0.25rem;">
                    <div style="width: ${analysis.pitch_intonation.pitch_stability_score * 100}%; height: 100%; background: #28a745; border-radius: 2px;"></div>
                </div>
            </div>
            
            <!-- Dynamic Range -->
            <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">Dynamic Range</div>
                <div style="font-weight: 600; font-size: 1rem;">${analysis.dynamics.dynamic_range_db.toFixed(1)} dB</div>
                <div style="font-size: 0.75rem; color: #999;">${analysis.dynamics.dynamic_range_category}</div>
            </div>
            
            <!-- Dynamic Contrast -->
            <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">Dynamic Contrast</div>
                <div style="font-weight: 600; font-size: 1rem;">${Math.round(analysis.dynamics.dynamic_contrast_score * 100)}%</div>
                <div style="width: 100%; height: 4px; background: #e0e0e0; border-radius: 2px; margin-top: 0.25rem;">
                    <div style="width: ${analysis.dynamics.dynamic_contrast_score * 100}%; height: 100%; background: #764ba2; border-radius: 2px;"></div>
                </div>
            </div>
            
            <!-- Articulation -->
            <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">Articulation</div>
                <div style="font-weight: 600; font-size: 1rem; text-transform: capitalize;">${analysis.articulation.predominant_articulation}</div>
            </div>
            
            <!-- Tone Quality -->
            <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">Tone Quality</div>
                <div style="font-weight: 600; font-size: 1rem; text-transform: capitalize;">${analysis.tone_quality.tonal_vs_noisy}</div>
            </div>
        </div>

        <!-- Performance Level and Difficulty -->
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: rgba(0, 177, 211, 0.05); border-radius: 8px; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 0.9rem; color: #666;">Performance Level:</span>
                <span style="padding: 0.5rem 1rem; background: rgba(102, 126, 234, 0.15); color: #667eea; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">${scores.performance_level}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 0.9rem; color: #666;">Difficulty:</span>
                <span style="padding: 0.5rem 1rem; background: rgba(255, 193, 7, 0.15); color: #f39c12; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">${scores.difficulty_estimate}</span>
            </div>
        </div>

        <!-- Four Pillars Scores -->
        <h4 style="font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem; color: #333;">Four Pillars Assessment</h4>
        <div class="result-item">
            <span class="result-number">${technicalSkills}</span>
            <span class="result-label">Technical Skills & Competence</span>
            <div class="result-bar">
                <div class="result-fill" style="width: ${technicalSkills}%"></div>
            </div>
        </div>
        <div class="result-item">
            <span class="result-number">${compositional}</span>
            <span class="result-label">Compositional & Musicianship</span>
            <div class="result-bar">
                <div class="result-fill" style="width: ${compositional}%"></div>
            </div>
        </div>
        <div class="result-item">
            <span class="result-number">${repertoire}</span>
            <span class="result-label">Repertoire & Cultural Knowledge</span>
            <div class="result-bar">
                <div class="result-fill" style="width: ${repertoire}%"></div>
            </div>
        </div>
        <div class="result-item">
            <span class="result-number">${performingArtistry}</span>
            <span class="result-label">Performing Artistry</span>
            <div class="result-bar">
                <div class="result-fill" style="width: ${performingArtistry}%"></div>
            </div>
        </div>
    `;
    
    // Display feedback
    const feedbackContainer = document.getElementById('aiCoachFeedbackContent');
    if (analysisResult.feedback) {
        feedbackContainer.innerHTML = analysisResult.feedback;
        feedbackContainer.style.whiteSpace = 'pre-wrap';
    }
    
    console.log('AI Coach Results displayed with full metrics scorecard');
}

async function submitAssignment() {
    const assignmentDetails = document.getElementById('assignmentDetails');
    const aiAnalysis = document.getElementById('aiAnalysis');
    
    // Switch to AI analysis page
    assignmentDetails.classList.remove('active');
    aiAnalysis.style.display = 'block';
    setTimeout(() => {
        aiAnalysis.classList.add('active');
    }, 50);
    
    // Call AI Coach API with the uploaded audio
    try {
        const result = await analyzeAudioWithAI(uploadedAudioFile);
        
        // Display results after analysis completes
        if (result.success) {
            displayAICoachResults(result);
            document.getElementById('analysisAnimation').style.display = 'none';
            document.getElementById('analysisResults').style.display = 'block';
        } else {
            throw new Error(result.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Error analyzing audio:', error);
        // Show error but still display mock results
        alert('AI analysis encountered an error: ' + error.message);
        setTimeout(() => {
            document.getElementById('analysisAnimation').style.display = 'none';
            document.getElementById('analysisResults').style.display = 'block';
        }, 2000);
    }
}

// AI Coach Integration
async function analyzeAudioWithAI(audioFile, options = {}) {
    if (!audioFile) {
        throw new Error('No audio file provided');
    }
    
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    
    // Optional context parameters
    if (options.piece_name) formData.append('piece_name', options.piece_name);
    if (options.composer) formData.append('composer', options.composer);
    if (options.student_notes) formData.append('student_notes', options.student_notes);
    
    try {
        const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.endpoints.aiCoach}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
                // Don't set Content-Type - browser will set it with boundary for FormData
            },
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('AI Coach API error:', error);
        throw error;
    }
}

// Store AI analysis results globally
let currentAIAnalysis = null;

function displayAICoachResults(analysisResult) {
    currentAIAnalysis = analysisResult;
    
    // Extract scores from audio_analysis
    const analysis = analysisResult.audio_analysis;
    if (!analysis) {
        console.error('No audio analysis data found');
        return;
    }
    
    const scores = analysis.performance_scores;
    
    // Map technical proficiency to Technical Skills
    const technicalSkills = Math.round(scores.technical_proficiency * 100);
    
    // Map expressiveness to Performing Artistry
    const performingArtistry = Math.round(scores.expressiveness * 100);
    
    // Calculate other pillars based on available metrics
    const compositional = Math.round((
        analysis.pitch_intonation.pitch_stability_score * 100 +
        analysis.musical_structure.musical_development_score * 100
    ) / 2);
    
    const repertoire = Math.round((
        analysis.dynamics.dynamic_contrast_score * 100 +
        analysis.tone_quality.brightness_consistency * 100
    ) / 2);
    
    const overall = Math.round(scores.overall_score * 100);
    
    // Update the DOM with actual scores
    const resultItems = document.querySelectorAll('.result-item');
    if (resultItems.length >= 4) {
        // Technical Skills
        updateResultItem(resultItems[0], technicalSkills, 'Technical Skills & Competence');
        
        // Compositional
        updateResultItem(resultItems[1], compositional, 'Compositional & Musicianship');
        
        // Repertoire
        updateResultItem(resultItems[2], repertoire, 'Repertoire & Cultural Knowledge');
        
        // Performing Artistry
        updateResultItem(resultItems[3], performingArtistry, 'Performing Artistry');
    }
    
    // Update overall score
    const overallScoreElement = document.querySelector('.overall-score h3');
    if (overallScoreElement) {
        overallScoreElement.textContent = `Overall Score: ${overall}/100`;
    }
    
    // Update feedback text
    const feedbackElement = document.querySelector('.overall-score p');
    if (feedbackElement && analysisResult.feedback) {
        // Extract first paragraph from feedback as summary
        const firstParagraph = analysisResult.feedback.split('\n\n')[0].replace(/^#+\s*/gm, '');
        feedbackElement.textContent = firstParagraph.substring(0, 200) + '...';
    }
    
    console.log('AI Coach Results displayed:', {
        technical: technicalSkills,
        compositional,
        repertoire,
        performing: performingArtistry,
        overall
    });
}

function updateResultItem(element, score, label) {
    const numberElement = element.querySelector('.result-number');
    const labelElement = element.querySelector('.result-label');
    const fillElement = element.querySelector('.result-fill');
    
    if (numberElement) numberElement.textContent = score;
    if (labelElement) labelElement.textContent = label;
    if (fillElement) fillElement.style.width = `${score}%`;
}

function closeAnalysisResults() {
    const studentDashboard = document.getElementById('studentDashboard');
    const aiAnalysis = document.getElementById('aiAnalysis');
    
    aiAnalysis.classList.remove('active');
    setTimeout(() => {
        aiAnalysis.style.display = 'none';
        studentDashboard.classList.add('active');
        // Reset for next time
        document.getElementById('analysisAnimation').style.display = 'block';
        document.getElementById('analysisResults').style.display = 'none';
    }, 250);
}

// AI Chat Functions
function openAIChat() {
    document.getElementById('aiChatOverlay').style.display = 'flex';
}

function closeAIChat() {
    document.getElementById('aiChatOverlay').style.display = 'none';
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    const messagesContainer = document.getElementById('chatMessages');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
        <div class="message-content">
            <p>${message}</p>
        </div>
    `;
    messagesContainer.appendChild(userMessage);
    
    // Clear input
    input.value = '';
    
    // Simulate AI response
    setTimeout(() => {
        const aiResponse = getAIResponse(message);
        const aiMessage = document.createElement('div');
        aiMessage.className = 'message ai-message';
        aiMessage.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <p>${aiResponse}</p>
            </div>
        `;
        messagesContainer.appendChild(aiMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 1000);
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function getAIResponse(userMessage) {
    const lowerMessage = userMessage.toLowerCase();
    
    // If we have real AI analysis feedback, use it intelligently
    if (currentAIAnalysis && currentAIAnalysis.feedback) {
        const feedback = currentAIAnalysis.feedback;
        
        // Check for specific keywords and extract relevant sections
        if (lowerMessage.includes('why')) {
            // Find and return priority improvements or overall assessment
            const lines = feedback.split('\n');
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].includes('Priority') || lines[i].includes('Improvement')) {
                    // Return next 3-5 lines as context
                    const context = lines.slice(i + 1, Math.min(i + 6, lines.length))
                        .filter(l => l.trim().length > 0)
                        .join(' ');
                    if (context.length > 0) {
                        return context.substring(0, 400) + (context.length > 400 ? '...' : '');
                    }
                }
            }
        }
        
        if (lowerMessage.includes('technical')) {
            // Extract technical analysis section
            const techMatch = feedback.match(/### ?Technical[\s\S]{0,500}?(?=###|$)/i);
            if (techMatch) {
                return techMatch[0].replace(/###/g, '').substring(0, 400);
            }
            return `Your technical proficiency is ${Math.round(currentAIAnalysis.audio_analysis.performance_scores.technical_proficiency * 100)}%. ` + 
                   'Check the full feedback for specific exercises to improve.';
        }
        
        if (lowerMessage.includes('practice') || lowerMessage.includes('how')) {
            // Extract practice plan
            const practiceMatch = feedback.match(/Practice Plan[\s\S]{0,600}?(?=##|$)/i);
            if (practiceMatch) {
                return practiceMatch[0].replace(/##/g, '').substring(0, 500);
            }
        }
        
        if (lowerMessage.includes('improve') || lowerMessage.includes('better')) {
            // Extract priority improvements
            const improveMatch = feedback.match(/Priority[\s\S]{0,500}?(?=##|$)/i);
            if (improveMatch) {
                return improveMatch[0].replace(/##/g, '').substring(0, 400);
            }
        }
        
        // Default: return first substantial paragraph
        const paragraphs = feedback.split('\n\n').filter(p => p.trim().length > 50);
        if (paragraphs.length > 1) {
            return paragraphs[1].replace(/^#+\s*/gm, '').substring(0, 400);
        }
    }
    
    // Fallback responses
    if (lowerMessage.includes('why')) {
        return 'Alex, really good lesson today. You\'re already playing this at a level where the next gains are about refinement of artistry, not "fixing". This week keep your focus on two things - keep the core of the sound absolutely steady through long notes, especially when you change string, don\'t let the bow "reset" the line. And Second, in the chordal and broken chord moments, make the harmony speak clearly, think bass first, then let the upper voice answer, so we hear the architecture. Also, watch the ends of notes, the releases in Bach are the punctuation, the silences have to feel intentional, not accidental. Keep vibrato tasteful, more like warmth on arrivals, less like a constant layer.';
    }
    
    const responses = {
        'technical': 'Your Technical Skills score shows strong finger positioning and scale execution. The areas for improvement include tempo consistency and articulation clarity.',
        'compositional': 'Your Compositional & Musicianship score indicates good understanding of musical structure. Focus on dynamic contrasts and phrasing to improve this area.',
        'repertoire': 'Great work on Repertoire & Cultural Knowledge! Your listening notes showed deep understanding of the musical period style.',
        'performing': 'Your Performing Artistry score reflects good musical expression. Work on dynamic control and emotional connection to improve further.',
        'improve': 'To improve your overall score, focus on: 1) Attack clarity and articulation, 2) Dynamic contrasts, 3) Tempo stability, and 4) Pitch intonation.',
        'practice': 'I recommend practicing with a metronome, listening to more master recordings, and working on articulation exercises. Aim for 30 minutes daily on technical work.'
    };
    
    if (lowerMessage.includes('technical')) return responses.technical;
    if (lowerMessage.includes('compositional') || lowerMessage.includes('musicianship')) return responses.compositional;
    if (lowerMessage.includes('repertoire') || lowerMessage.includes('cultural')) return responses.repertoire;
    if (lowerMessage.includes('performing') || lowerMessage.includes('artistry')) return responses.performing;
    if (lowerMessage.includes('improve') || lowerMessage.includes('better')) return responses.improve;
    if (lowerMessage.includes('practice') || lowerMessage.includes('how')) return responses.practice;
    
    return 'Great question! Your overall performance shows strong progress. Which specific area would you like to discuss - Technical Skills, Compositional & Musicianship, Repertoire & Cultural Knowledge, or Performing Artistry?';
}

// Class Report Functions
function openClassReport() {
    const teacherDashboard = document.getElementById('teacherDashboard');
    const classReport = document.getElementById('classReport');
    
    teacherDashboard.classList.remove('active');
    classReport.style.display = 'block';
    setTimeout(() => {
        classReport.classList.add('active');
    }, 50);
}

function closeClassReport() {
    const teacherDashboard = document.getElementById('teacherDashboard');
    const classReport = document.getElementById('classReport');
    
    classReport.classList.remove('active');
    setTimeout(() => {
        classReport.style.display = 'none';
        teacherDashboard.classList.add('active');
    }, 250);
}

// Progress History Functions
function openProgressHistory() {
    const studentDashboard = document.getElementById('studentDashboard');
    const progressHistory = document.getElementById('progressHistory');
    
    studentDashboard.classList.remove('active');
    progressHistory.style.display = 'block';
    setTimeout(() => {
        progressHistory.classList.add('active');
        initializeChartInteractivity();
    }, 50);
}

function closeProgressHistory() {
    const studentDashboard = document.getElementById('studentDashboard');
    const progressHistory = document.getElementById('progressHistory');
    
    progressHistory.classList.remove('active');
    setTimeout(() => {
        progressHistory.style.display = 'none';
        studentDashboard.classList.add('active');
    }, 250);
}

function initializeChartInteractivity() {
    const dataPoints = document.querySelectorAll('.data-point');
    const tooltip = document.getElementById('chartTooltip');
    
    dataPoints.forEach(point => {
        point.addEventListener('mouseenter', function(e) {
            const value = this.getAttribute('data-value');
            const date = this.getAttribute('data-date');
            const rect = this.getBoundingClientRect();
            const container = document.querySelector('.chart-container').getBoundingClientRect();
            
            tooltip.innerHTML = `<strong>${date}</strong><br>Score: ${value}`;
            tooltip.style.left = (rect.left - container.left + 10) + 'px';
            tooltip.style.top = (rect.top - container.top - 50) + 'px';
            tooltip.classList.add('show');
        });
        
        point.addEventListener('mouseleave', function() {
            tooltip.classList.remove('show');
        });
    });
}
