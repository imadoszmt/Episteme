// Theme handling
document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    const icon = themeToggle?.querySelector('i');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    // Theme toggle click handler
    themeToggle?.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        if (!icon) return;
        icon.className = theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation classes to cards
    const cards = document.querySelectorAll('.card');
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('card-animate');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        observer.observe(card);
    });

    // Add hover effect to navigation items
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'translateY(-2px)';
            item.style.transition = 'transform 0.2s ease';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'translateY(0)';
        });
    });

    // Alert auto-dismiss
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => {
                alert.remove();
            }, 150);
        }, 5000);
    });
});

// Quiz-specific functionality
if (document.querySelector('.quiz-container')) {
    // Timer functionality
    let timer;
    let seconds = 0;

    function startTimer() {
        timer = setInterval(() => {
            seconds++;
            const timerDisplay = document.querySelector('#timer span');
            if (timerDisplay) {
                timerDisplay.textContent = new Date(seconds * 1000).toISOString().substr(14, 5);
            }
        }, 1000);
    }

    // Option selection
    function selectOption(element, optionId) {
        document.querySelectorAll('.option-item').forEach(item => {
            item.classList.remove('selected');
        });
        element.classList.add('selected');
        const input = element.querySelector('input');
        if (input) {
            input.checked = true;
        }
    }

    // Form submission
    function submitAnswer() {
        const form = document.getElementById('questionForm');
        if (form) {
            const selectedOption = form.querySelector('input[name="answer"]:checked');
            if (selectedOption) {
                form.submit();
            } else {
                alert('Please select an answer');
            }
        }
    }

    // Initialize quiz features
    startTimer();
}

// Add custom styles for primary color elements
document.documentElement.style.setProperty('--primary-color', '#8A6534');
document.documentElement.style.setProperty('--primary-hover', '#735425');

// Add smooth transitions for theme changes
document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
