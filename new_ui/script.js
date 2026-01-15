// API Configuration Helper
function getApiConfig() {
    // Wait for config to load if necessary
    if (window.RIAM_CONFIG?.isLoading) {
        console.warn('[API] Config still loading, using defaults');
    }
    
    // Use loaded config or fallback to defaults
    return {
        baseURL: window.RIAM_CONFIG?.apiBaseUrl || 'http://localhost:8000',
        endpoints: window.RIAM_CONFIG?.endpoints || {
            aiCoach: '/ai-coach/analyze',
            aiCoachChat: '/ai-coach/chat',
            login: '/auth/login',
            me: '/auth/me'
        }
    };
}

// Legacy support - API_CONFIG as getter
const API_CONFIG = new Proxy({}, {
    get(target, prop) {
        return getApiConfig()[prop];
    }
});

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
    const allPages = ['studentDashboard', 'teacherDashboard', 'sessionDetails', 'assignmentDetails', 'aiAnalysis', 'classReport', 'progressHistory', 'aiCoachPage', 'studentAssessmentReview'];
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
let conversationHistory = [];  // Track chat history

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
    
    // Initialize chat if there's analysis context
    if (currentAIAnalysis && conversationHistory.length === 0) {
        const messagesContainer = document.getElementById('chatMessages');
        // Clear any existing messages except the welcome message
        const welcomeMsg = messagesContainer.querySelector('.ai-message:first-child');
        messagesContainer.innerHTML = '';
        if (welcomeMsg) {
            messagesContainer.appendChild(welcomeMsg);
        }
    }
}

function closeAIChat() {
    document.getElementById('aiChatOverlay').style.display = 'none';
    // Reset conversation when closing (optional - remove if you want to keep history)
    // conversationHistory = [];
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const messagesContainer = document.getElementById('chatMessages');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to conversation history
    conversationHistory.push({
        role: 'user',
        content: message
    });
    
    // Add user message to UI
    const userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    messagesContainer.appendChild(userMessage);
    
    // Clear input
    input.value = '';
    
    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message ai-message typing-indicator';
    typingIndicator.id = 'typingIndicator';
    typingIndicator.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingIndicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    try {
        // Prepare analysis context if available
        const analysisContext = currentAIAnalysis ? {
            feedback: currentAIAnalysis.feedback,
            audio_analysis: currentAIAnalysis.audio_analysis
        } : null;
        
        const requestBody = {
            question: message,
            analysis_context: analysisContext,
            conversation_history: conversationHistory.slice(0, -1) // Exclude current message
        };
        
        console.log('[Chat] Sending request:', {
            url: `${API_CONFIG.baseURL}${API_CONFIG.endpoints.aiCoachChat}`,
            hasAuth: !!authToken,
            hasAnalysisContext: !!analysisContext,
            historyLength: conversationHistory.length
        });
        
        // Call the API
        const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.endpoints.aiCoachChat}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(requestBody)
        });
        
        console.log('[Chat] Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('[Chat] Error response:', errorText);
            throw new Error(`API error: ${response.status} - ${errorText}`);
        }
        
        const data = await response.json();
        console.log('[Chat] Response data:', data);
        
        // Remove typing indicator
        typingIndicator.remove();
        
        if (data.success && data.response) {
            // Add assistant response to conversation history
            conversationHistory.push({
                role: 'assistant',
                content: data.response
            });
            
            // Add AI response to UI
            const aiMessage = document.createElement('div');
            aiMessage.className = 'message ai-message';
            aiMessage.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>${formatAIResponse(data.response)}</p>
                </div>
            `;
            messagesContainer.appendChild(aiMessage);
        } else {
            throw new Error(data.error || 'Failed to get response');
        }
        
    } catch (error) {
        console.error('Chat error:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack,
            authToken: authToken ? 'present' : 'missing',
            apiUrl: `${API_CONFIG.baseURL}${API_CONFIG.endpoints.aiCoachChat}`,
            hasAnalysisContext: !!currentAIAnalysis
        });
        
        // Remove typing indicator
        const indicator = document.getElementById('typingIndicator');
        if (indicator) indicator.remove();
        
        // Show error message with more details in console
        const errorMessage = document.createElement('div');
        errorMessage.className = 'message ai-message error-message';
        errorMessage.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-exclamation-circle"></i>
            </div>
            <div class="message-content">
                <p>Sorry, I couldn't process your question. Please try again.</p>
                <small style="color: #999; font-size: 0.8rem;">Check browser console for details (F12)</small>
            </div>
        `;
        messagesContainer.appendChild(errorMessage);
    }
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Helper function to format AI response (convert markdown-like formatting to HTML)
function formatAIResponse(text) {
    // Escape HTML first
    text = escapeHtml(text);
    
    // Convert **bold** to <strong>
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
    
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
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

// ==========================================
// Teacher Review Flow Functions
// ==========================================

// Submit recording for teacher review (instead of AI analysis)
async function submitForTeacherReview() {
    if (!uploadedAudioFile) {
        alert('Please select an audio file first!');
        return;
    }
    
    console.log('Submitting recording for teacher review...');
    
    // Get context from form
    const pieceName = document.getElementById('aiCoachPieceName').value.trim();
    const composer = document.getElementById('aiCoachComposer').value.trim();
    const notes = document.getElementById('aiCoachNotes').value.trim();
    
    // Hide form, show loading
    document.getElementById('aiCoachForm').style.display = 'none';
    document.getElementById('aiCoachLoading').style.display = 'block';
    
    try {
        // Still call the AI analysis API in the background for the teacher
        const result = await analyzeAudioWithAI(uploadedAudioFile, {
            piece_name: pieceName || undefined,
            composer: composer || undefined,
            student_notes: notes || undefined
        });
        
        console.log('Analysis complete (for teacher):', result);
        
        // Store the result for when teacher views it
        if (result.success) {
            // Store in localStorage for demo purposes
            localStorage.setItem('pendingStudentSubmission', JSON.stringify({
                studentName: currentUser?.name || 'Alex Johnson',
                fileName: uploadedAudioFile.name,
                timestamp: new Date().toISOString(),
                analysisResult: result
            }));
        }
        
        // Show submission success message to student
        document.getElementById('aiCoachLoading').style.display = 'none';
        document.getElementById('aiCoachSubmissionSuccess').style.display = 'block';
        
        // Update the filename in success message
        document.getElementById('submittedFileName').textContent = uploadedAudioFile.name;
        
        // Add a new entry to the teacher's pending assignments (stored in localStorage)
        addPendingAssignment({
            studentName: currentUser?.name || 'Alex Johnson',
            assignmentName: pieceName || 'Audio Recording',
            fileName: uploadedAudioFile.name,
            submittedAt: 'Just now'
        });
        
    } catch (error) {
        console.error('Error during submission:', error);
        // Still show success to student (for demo robustness)
        document.getElementById('aiCoachLoading').style.display = 'none';
        document.getElementById('aiCoachSubmissionSuccess').style.display = 'block';
        document.getElementById('submittedFileName').textContent = uploadedAudioFile.name;
        
        // Add pending assignment anyway for demo
        addPendingAssignment({
            studentName: currentUser?.name || 'Alex Johnson',
            assignmentName: 'Audio Recording',
            fileName: uploadedAudioFile.name,
            submittedAt: 'Just now'
        });
    }
}

// Add a pending assignment to the teacher's view
function addPendingAssignment(assignment) {
    // Get existing assignments from localStorage
    let pendingAssignments = JSON.parse(localStorage.getItem('pendingTeacherAssignments') || '[]');
    
    // Add new assignment at the beginning
    pendingAssignments.unshift({
        id: Date.now(),
        ...assignment
    });
    
    // Keep only last 10 for demo
    pendingAssignments = pendingAssignments.slice(0, 10);
    
    // Save back to localStorage
    localStorage.setItem('pendingTeacherAssignments', JSON.stringify(pendingAssignments));
    
    console.log('Added pending assignment:', assignment);
}

// Return to student dashboard from submission success
function returnToStudentDashboard() {
    const aiCoachPage = document.getElementById('aiCoachPage');
    const studentDashboard = document.getElementById('studentDashboard');
    
    if (aiCoachPage) {
        aiCoachPage.classList.remove('active');
        setTimeout(() => {
            aiCoachPage.style.display = 'none';
            
            // Reset all states
            document.getElementById('aiCoachForm').style.display = 'block';
            document.getElementById('aiCoachLoading').style.display = 'none';
            document.getElementById('aiCoachResults').style.display = 'none';
            document.getElementById('aiCoachSubmissionSuccess').style.display = 'none';
            
            // Clear form
            document.getElementById('aiCoachPieceName').value = '';
            document.getElementById('aiCoachComposer').value = '';
            document.getElementById('aiCoachNotes').value = '';
            document.getElementById('aiCoachAudioName').textContent = '';
            uploadedAudioFile = null;
            
            // Show student dashboard
            if (studentDashboard) {
                studentDashboard.classList.add('active');
            }
        }, 250);
    }
}

// Open student assessment review page (teacher view)
function openStudentAssessmentReview() {
    const teacherDashboard = document.getElementById('teacherDashboard');
    const studentAssessmentReview = document.getElementById('studentAssessmentReview');
    
    if (teacherDashboard) {
        teacherDashboard.classList.remove('active');
    }
    
    if (studentAssessmentReview) {
        studentAssessmentReview.style.display = 'block';
        setTimeout(() => {
            studentAssessmentReview.classList.add('active');
        }, 50);
    }
}

// Close student assessment review page
function closeStudentAssessmentReview() {
    const teacherDashboard = document.getElementById('teacherDashboard');
    const studentAssessmentReview = document.getElementById('studentAssessmentReview');
    
    if (studentAssessmentReview) {
        studentAssessmentReview.classList.remove('active');
        setTimeout(() => {
            studentAssessmentReview.style.display = 'none';
            
            if (teacherDashboard) {
                teacherDashboard.classList.add('active');
            }
        }, 250);
    }
}

// Approve student assessment and send feedback
function approveStudentAssessment() {
    const teacherComments = document.getElementById('teacherComments')?.value || '';
    
    // Show success animation
    const studentAssessmentReview = document.getElementById('studentAssessmentReview');
    if (studentAssessmentReview) {
        // Create success overlay
        const successOverlay = document.createElement('div');
        successOverlay.className = 'success-message';
        successOverlay.style.display = 'block';
        successOverlay.innerHTML = `
            <div class="success-content">
                <i class="fas fa-check-circle"></i>
                <h3>Assessment Approved!</h3>
                <p>The feedback has been sent to Alex Johnson and will appear in their dashboard.</p>
            </div>
        `;
        
        studentAssessmentReview.querySelector('.session-content').appendChild(successOverlay);
        
        // Return to dashboard after 2 seconds
        setTimeout(() => {
            closeStudentAssessmentReview();
            successOverlay.remove();
            
            // Clear the teacher comments
            if (document.getElementById('teacherComments')) {
                document.getElementById('teacherComments').value = '';
            }
        }, 2000);
    }
    
    console.log('Assessment approved with comments:', teacherComments);
}
