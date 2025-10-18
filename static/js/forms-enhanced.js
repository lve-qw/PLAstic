// Enhanced form functionality
class FormEnhancer {
    constructor() {
        this.setupPasswordToggle();
        this.setupRealTimeValidation();
        this.setupFormAnimations();
    }

    // Password visibility toggle
    setupPasswordToggle() {
        document.querySelectorAll('input[type="password"]').forEach(input => {
            const wrapper = input.closest('.form__input-wrapper');
            if (!wrapper) return;

            const toggle = document.createElement('button');
            toggle.type = 'button';
            toggle.className = 'form__password-toggle';
            toggle.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                </svg>
            `;

            toggle.addEventListener('click', () => {
                const isPassword = input.type === 'password';
                input.type = isPassword ? 'text' : 'password';
                
                // Update icon
                if (isPassword) {
                    toggle.innerHTML = `
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/>
                            <line x1="1" y1="1" x2="23" y2="23"/>
                        </svg>
                    `;
                } else {
                    toggle.innerHTML = `
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                            <circle cx="12" cy="12" r="3"/>
                        </svg>
                    `;
                }
            });

            wrapper.appendChild(toggle);
        });
    }

    // Real-time form validation
    setupRealTimeValidation() {
        document.querySelectorAll('.form__input').forEach(input => {
            input.addEventListener('input', this.debounce(() => {
                this.validateField(input);
            }, 300));

            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });
    }

    // Form animations and enhancements
    setupFormAnimations() {
        // Add focus states with animation
        document.querySelectorAll('.form__input').forEach(input => {
            input.addEventListener('focus', () => {
                input.parentElement.classList.add('focused');
            });

            input.addEventListener('blur', () => {
                input.parentElement.classList.remove('focused');
            });
        });

        // Animate form groups on appearance
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'slideUp 0.6s ease forwards';
                    observer.unobserve(entry.target);
                }
            });
        });

        document.querySelectorAll('.form__group').forEach((group, index) => {
            group.style.opacity = '0';
            group.style.transform = 'translateY(20px)';
            observer.observe(group);
        });
    }

    // Enhanced field validation
    validateField(field) {
        const value = field.value.trim();
        const group = field.closest('.form__group');
        const errorElement = group?.querySelector('.form__error');

        // Clear previous state
        field.classList.remove('error', 'success');
        group?.classList.remove('has-error', 'has-success');

        // Skip validation if field is empty and not required
        if (!value && !field.hasAttribute('required')) {
            return true;
        }

        let isValid = true;
        let errorMessage = '';

        // Required validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'Это поле обязательно для заполнения';
        }

        // Email validation
        else if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Введите корректный email адрес';
            }
        }

        // Password strength validation
        else if (field.type === 'password' && value) {
            const strength = this.checkPasswordStrength(value);
            if (strength.score < 2) {
                isValid = false;
                errorMessage = 'Пароль слишком слабый';
            }
        }

        // Username validation
        else if (field.name === 'username' && value) {
            const usernameRegex = /^[a-zA-Z0-9_]+$/;
            if (!usernameRegex.test(value)) {
                isValid = false;
                errorMessage = 'Имя пользователя может содержать только буквы, цифры и подчеркивания';
            } else if (value.length < 3) {
                isValid = false;
                errorMessage = 'Имя пользователя должно содержать минимум 3 символа';
            }
        }

        // Update field state
        if (!isValid) {
            field.classList.add('error');
            group?.classList.add('has-error');
            if (errorElement) {
                errorElement.textContent = errorMessage;
                errorElement.style.display = 'flex';
            }
        } else {
            field.classList.add('success');
            group?.classList.add('has-success');
            if (errorElement) {
                errorElement.style.display = 'none';
            }
        }

        return isValid;
    }

    // Password strength checker
    checkPasswordStrength(password) {
        let score = 0;
        const suggestions = [];

        // Length check
        if (password.length >= 8) score++;
        else suggestions.push('Добавьте еще символов (минимум 8)');

        // Lowercase check
        if (/[a-z]/.test(password)) score++;
        else suggestions.push('Добавьте строчные буквы');

        // Uppercase check
        if (/[A-Z]/.test(password)) score++;
        else suggestions.push('Добавьте заглавные буквы');

        // Numbers check
        if (/[0-9]/.test(password)) score++;
        else suggestions.push('Добавьте цифры');

        // Special characters check
        if (/[^a-zA-Z0-9]/.test(password)) score++;
        else suggestions.push('Добавьте специальные символы');

        return { score, suggestions };
    }

    // Utility function for debouncing
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FormEnhancer();
});

// Add CSS animations
const formStyles = document.createElement('style');
formStyles.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .form__group {
        animation-delay: calc(var(--index, 0) * 0.1s);
    }

    .form__input-wrapper.focused .form__input {
        transform: translateY(-1px);
    }

    .form__group.has-success .form__input {
        border-color: var(--success-color, #10b981);
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }

    .form__group.has-error .form__input {
        border-color: var(--error-color, #ef4444);
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
    }
`;
document.head.appendChild(formStyles);