/*
MZB_ Main JavaScript
HUMAN_DECISION: Interactive features, animations, AJAX where needed
*/

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
    
    // Add hover animation to all cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function(e) {
            this.style.transition = 'all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1)';
        });
    });
    
    // Celebration Wall confetti effect on load
    if (window.location.pathname.includes('/celebration/wall')) {
        const celebrationCards = document.querySelectorAll('.celebration-card');
        if (celebrationCards.length > 0) {
            triggerConfetti();
        }
    }
    
    // Project stage update visual feedback
    const stageSelects = document.querySelectorAll('.stage-select');
    stageSelects.forEach(select => {
        select.addEventListener('change', function() {
            const badge = this.closest('.card')?.querySelector('.stage-badge');
            if (badge) {
                badge.style.transform = 'scale(1.1)';
                setTimeout(() => badge.style.transform = '', 300);
            }
        });
    });
});

// Confetti effect for celebration wall
function triggerConfetti() {
    if (typeof confetti === 'function') {
        confetti({
            particleCount: 150,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#2E7D32', '#4CAF50', '#1B5E20', '#81C784']
        });
        
        setTimeout(() => {
            confetti({
                particleCount: 100,
                spread: 100,
                origin: { y: 0.7, x: 0.3 },
                colors: ['#2E7D32', '#4CAF50']
            });
        }, 200);
    }
}

// Raise hand animation
function raiseHandAnimation(button) {
    button.innerHTML = '🤚 Hand Raised!';
    button.disabled = true;
    button.style.transform = 'scale(0.95)';
    
    setTimeout(() => {
        button.style.transform = '';
    }, 200);
}

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            input.style.borderColor = '';
        }
    });
    
    return isValid;
}

// Live search for feed (bonus feature)
function filterFeed(searchTerm) {
    const feedItems = document.querySelectorAll('.feed-item, .feed-card');
    const term = searchTerm.toLowerCase();
    
    feedItems.forEach(item => {
        const text = item.innerText.toLowerCase();
        if (text.includes(term)) {
            item.style.display = '';
            item.style.animation = 'slideUp 0.3s ease-out';
        } else {
            item.style.display = 'none';
        }
    });
}

// Progress update animation
function updateProgress(projectId, milestoneText) {
    const milestoneList = document.querySelector(`#milestones-${projectId}`);
    if (milestoneList) {
        const newMilestone = document.createElement('div');
        newMilestone.className = 'comment-box slide-right';
        newMilestone.innerHTML = `🏆 ${milestoneText}`;
        milestoneList.prepend(newMilestone);
        
        setTimeout(() => newMilestone.style.opacity = '1', 10);
    }
}