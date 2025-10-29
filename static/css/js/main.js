// Main JavaScript functionality for Resume Analyzer

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // File upload validation and preview
    const resumeInput = document.getElementById('resume');
    if (resumeInput) {
        resumeInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file size (16MB max)
                const maxSize = 16 * 1024 * 1024;
                if (file.size > maxSize) {
                    alert('File size too large. Maximum allowed size is 16MB.');
                    this.value = '';
                    return;
                }

                // Validate file type
                if (file.type !== 'application/pdf') {
                    alert('Only PDF files are allowed.');
                    this.value = '';
                    return;
                }

                // Update UI to show selected file
                const fileName = file.name;
                const fileSize = (file.size / 1024 / 1024).toFixed(2);
                console.log(`Selected file: ${fileName} (${fileSize} MB)`);
            }
        });
    }

    // Job description character counter
    const jobDescTextarea = document.getElementById('job_description');
    if (jobDescTextarea) {
        const charCountDisplay = document.createElement('div');
        charCountDisplay.className = 'form-text mt-1';
        charCountDisplay.innerHTML = '<i class="fas fa-keyboard me-1"></i>0 characters';
        jobDescTextarea.parentNode.appendChild(charCountDisplay);

        jobDescTextarea.addEventListener('input', function() {
            const charCount = this.value.length;
            charCountDisplay.innerHTML = `<i class="fas fa-keyboard me-1"></i>${charCount.toLocaleString()} characters`;
            
            // Change color based on length
            if (charCount < 500) {
                charCountDisplay.className = 'form-text mt-1 text-warning';
                charCountDisplay.innerHTML += ' (Consider adding more details for better analysis)';
            } else if (charCount > 5000) {
                charCountDisplay.className = 'form-text mt-1 text-info';
                charCountDisplay.innerHTML += ' (Very detailed - excellent for analysis!)';
            } else {
                charCountDisplay.className = 'form-text mt-1 text-success';
                charCountDisplay.innerHTML += ' (Good length for analysis)';
            }
        });
    }

    // Form submission handling with loading state
    const analyzeForm = document.getElementById('analyzeForm');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function(e) {
            const submitBtn = document.getElementById('submitBtn');
            const resumeFile = document.getElementById('resume').files[0];
            const jobDesc = document.getElementById('job_description').value.trim();

            // Final validation
            if (!resumeFile) {
                e.preventDefault();
                alert('Please select a resume file.');
                return;
            }

            if (!jobDesc) {
                e.preventDefault();
                alert('Please enter a job description.');
                return;
            }

            if (jobDesc.length < 100) {
                e.preventDefault();
                alert('Job description seems too short. Please provide more details for accurate analysis.');
                return;
            }

            // Show loading state
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing Resume...';
            submitBtn.disabled = true;

            // Show progress indicator
            showAnalysisProgress();
        });
    }

    // Enhanced badge interactions
    document.querySelectorAll('.badge').forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Results page enhancements
    if (document.querySelector('.score-reveal')) {
        // Animate score reveal
        setTimeout(() => {
            document.querySelectorAll('.score-reveal').forEach(el => {
                el.classList.add('animate__animated', 'animate__fadeInUp');
            });
        }, 100);
    }

    // Copy functionality for keywords
    document.querySelectorAll('.badge').forEach(badge => {
        badge.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(() => {
                // Show temporary feedback
                const originalBg = this.style.backgroundColor;
                this.style.backgroundColor = '#28a745';
                setTimeout(() => {
                    this.style.backgroundColor = originalBg;
                }, 200);
            }).catch(() => {
                console.log('Could not copy text');
            });
        });
        
        // Add cursor pointer and title
        badge.style.cursor = 'pointer';
        badge.title = 'Click to copy';
    });
});

// Analysis progress indicator
function showAnalysisProgress() {
    const progressSteps = [
        'Extracting text from PDF...',
        'Processing resume with NLP...',
        'Analyzing job description...',
        'Comparing skills and keywords...',
        'Calculating compatibility scores...',
        'Generating improvement suggestions...',
        'Preparing results...'
    ];

    // Create progress modal
    const progressModal = document.createElement('div');
    progressModal.className = 'modal fade';
    progressModal.id = 'progressModal';
    progressModal.setAttribute('data-bs-backdrop', 'static');
    progressModal.setAttribute('data-bs-keyboard', 'false');
    
    progressModal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-body text-center p-4">
                    <div class="mb-4">
                        <i class="fas fa-cogs fa-3x text-primary mb-3"></i>
                        <h4>Analyzing Your Resume</h4>
                        <p class="text-muted">Please wait while we process your information...</p>
                    </div>
                    <div class="progress mb-3" style="height: 6px;">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                             role="progressbar" style="width: 0%"></div>
                    </div>
                    <div id="progressStep" class="text-muted small">
                        Initializing analysis...
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(progressModal);
    
    const modal = new bootstrap.Modal(progressModal);
    modal.show();
    
    // Simulate progress updates
    let currentStep = 0;
    const progressBar = progressModal.querySelector('.progress-bar');
    const stepText = progressModal.querySelector('#progressStep');
    
    const updateProgress = () => {
        if (currentStep < progressSteps.length) {
            const progress = ((currentStep + 1) / progressSteps.length) * 100;
            progressBar.style.width = progress + '%';
            stepText.textContent = progressSteps[currentStep];
            currentStep++;
            setTimeout(updateProgress, 1000 + Math.random() * 1000); // Variable timing for realism
        }
    };
    
    setTimeout(updateProgress, 500);
}

// Utility functions
function formatNumber(num) {
    return num.toLocaleString();
}

function getScoreColor(score) {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
}

function getScoreIcon(score) {
    if (score >= 80) return 'fas fa-trophy';
    if (score >= 60) return 'fas fa-thumbs-up';
    return 'fas fa-exclamation-triangle';
}

// Export functions for potential future use
window.ResumeAnalyzer = {
    formatNumber,
    getScoreColor,
    getScoreIcon,
    showAnalysisProgress
};
