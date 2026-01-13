// Dashboard functionality
function dashboard() {
    return {
        user: null,
        audioFile: null,
        aiCoachForm: {
            piece_name: '',
            composer: '',
            student_notes: ''
        },
        aiCoachLoading: false,
        aiFeedback: null,
        audioAnalysis: null,
        aiCoachError: null,
        
        async init() {
            if (!requireAuth()) return;
            
            this.user = getCurrentUser();
            document.getElementById('userNameDisplay').textContent = this.user.name || 'User';
        },
        
        async submitAICoach() {
            this.aiCoachLoading = true;
            this.aiCoachError = null;
            this.aiFeedback = null;
            this.audioAnalysis = null;
            
            try {
                const formData = new FormData();
                formData.append('audio_file', this.audioFile);
                
                if (this.aiCoachForm.piece_name) {
                    formData.append('piece_name', this.aiCoachForm.piece_name);
                }
                if (this.aiCoachForm.composer) {
                    formData.append('composer', this.aiCoachForm.composer);
                }
                if (this.aiCoachForm.student_notes) {
                    formData.append('student_notes', this.aiCoachForm.student_notes);
                }
                
                const response = await fetch(`${API_BASE_URL}/ai-coach/analyze`, {
                    method: 'POST',
                    headers: getAuthHeaders(),
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    this.aiFeedback = data.feedback;
                    this.audioAnalysis = data.audio_analysis;
                    
                    // Reset form
                    this.aiCoachForm = {
                        piece_name: '',
                        composer: '',
                        student_notes: ''
                    };
                    this.audioFile = null;
                    
                    // Reset file input
                    const fileInput = document.querySelector('input[type="file"]');
                    if (fileInput) fileInput.value = '';
                } else {
                    this.aiCoachError = data.error || data.detail || 'Failed to analyze performance. Please try again.';
                }
            } catch (error) {
                console.error('Error submitting to AI coach:', error);
                this.aiCoachError = 'Network error. Please check your connection and try again.';
            } finally {
                this.aiCoachLoading = false;
            }
        },
        
        formatFeedback(feedback) {
            if (!feedback) return '';
            return feedback
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\n/g, '<br>');
        },
        
        getScore(data, category, field) {
            if (!data || !data[category] || data[category][field] === undefined) return 'N/A';
            const value = data[category][field];
            if (typeof value === 'number' && value <= 1) {
                return Math.round(value * 100) + '%';
            }
            return value;
        },
        
        getNumericScore(data, category, field) {
            if (!data || !data[category] || data[category][field] === undefined) return 0;
            const value = data[category][field];
            return typeof value === 'number' ? value : 0;
        },
        
        getValue(data, category, field) {
            if (!data || !data[category] || data[category][field] === undefined) return 'N/A';
            return data[category][field];
        }
    }
}
