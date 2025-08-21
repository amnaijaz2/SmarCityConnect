// Tab Switching Functionality
function switchTab(tabName) {
    // Hide all panes and remove active classes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.style.display = 'none';
        pane.classList.remove('active');
    });
    
    // Show selected pane
    const activePane = document.getElementById(`${tabName}-pane`);
    if (activePane) {
        activePane.style.display = 'block';
        activePane.classList.add('active');
    }
    
    // Update tab buttons
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    const activeTab = document.getElementById(`${tabName}-tab`);
    if (activeTab) {
        activeTab.classList.add('active');
    }
}

// Animation on Scroll Functionality
function setupScrollAnimations() {
    const animateElements = document.querySelectorAll('.animate__animated');
    
    // Initialize elements as invisible
    animateElements.forEach(element => {
        element.style.visibility = 'hidden';
    });
    
    const animateOnScroll = function() {
        animateElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.style.visibility = 'visible';
                const animationClass = element.getAttribute('data-animate');
                if (animationClass) {
                    element.classList.add(animationClass);
                }
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Trigger once on load
}

// Smooth Scrolling for Anchor Links
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize first tab
    const defaultTabPane = document.getElementById('providers-pane');
    if (defaultTabPane) {
        defaultTabPane.style.display = 'block';
    }
    
    setupScrollAnimations();
    setupSmoothScrolling();
});