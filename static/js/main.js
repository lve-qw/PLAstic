// Main JavaScript application
class FilamentStoreApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupMobileMenu();
        this.setupAlerts();
        this.setupForms();
        this.setupInteractiveElements();
    }

    // Mobile menu functionality
    setupMobileMenu() {
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.getElementById('nav-menu');

        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
            });

            // Close menu when clicking on links
            document.querySelectorAll('.nav__link').forEach(link => {
                link.addEventListener('click', () => {
                    navMenu.classList.remove('active');
                    navToggle.classList.remove('active');
                });
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                    navMenu.classList.remove('active');
                    navToggle.classList.remove('active');
                }
            });
        }
    }

    // Alert system
    setupAlerts() {
        document.addEventListener('DOMContentLoaded', () => {
            const alerts = document.querySelectorAll('.alert');
            
            alerts.forEach(alert => {
                const closeBtn = alert.querySelector('.alert__close');
                if (closeBtn) {
                    closeBtn.addEventListener('click', () => {
                        alert.style.animation = 'slideOut 0.3s ease';
                        setTimeout(() => {
                            alert.remove();
                        }, 300);
                    });
                }

                // Auto-remove alerts after 5 seconds
                setTimeout(() => {
                    if (alert.parentElement) {
                        alert.style.animation = 'slideOut 0.3s ease';
                        setTimeout(() => {
                            alert.remove();
                        }, 300);
                    }
                }, 5000);
            });
        });
    }

    // Form enhancements
    setupForms() {
        // Add loading states to forms
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.classList.add('btn--loading');
                    submitBtn.disabled = true;
                }
            });
        });

        // Form validation enhancements
        document.querySelectorAll('.form__input').forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });

            input.addEventListener('input', () => {
                if (input.classList.contains('error')) {
                    this.validateField(input);
                }
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const group = field.closest('.form__group');
        const errorElement = group?.querySelector('.form__error');

        // Basic required validation
        if (field.hasAttribute('required') && !value) {
            field.classList.add('error');
            if (errorElement) {
                errorElement.textContent = 'Это поле обязательно для заполнения';
            }
            return false;
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                field.classList.add('error');
                if (errorElement) {
                    errorElement.textContent = 'Введите корректный email адрес';
                }
                return false;
            }
        }

        // Clear error state
        field.classList.remove('error');
        if (errorElement) {
            errorElement.textContent = '';
        }
        return true;
    }

    // Interactive elements
    setupInteractiveElements() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
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

        // Card hover effects
        document.querySelectorAll('.card--interactive').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-4px)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });
    }

    // Utility method to show toast messages
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `alert alert--${type}`;
        toast.innerHTML = `
            <span class="alert__message">${message}</span>
            <button class="alert__close" type="button">&times;</button>
        `;

        const messagesContainer = document.querySelector('.messages') || document.body;
        messagesContainer.appendChild(toast);

        this.setupAlerts(); // Re-initialize alerts for the new toast
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.filamentStoreApp = new FilamentStoreApp();
});

// Add CSS animation for alert removal
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(style);