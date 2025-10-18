// Функции для работы с иконками корзины
class CartIcons {
    // Анимация добавления в корзину
    static animateAdd(cartIcon) {
        cartIcon.classList.add('cart-animate');
        setTimeout(() => {
            cartIcon.classList.remove('cart-animate');
        }, 600);
    }

    // Обновление счетчика корзины
    static updateBadge(count) {
        const badges = document.querySelectorAll('.cart-badge');
        badges.forEach(badge => {
            badge.setAttribute('data-count', count);
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        });
    }

    // Показ мини-корзины при наведении
    static initHoverCart() {
        const cartIcons = document.querySelectorAll('.cart-icon[data-hover]');
        
        cartIcons.forEach(icon => {
            icon.addEventListener('mouseenter', function() {
                this.classList.add('cart-hover');
            });
            
            icon.addEventListener('mouseleave', function() {
                this.classList.remove('cart-hover');
            });
        });
    }

    // Быстрое добавление в корзину
    static initQuickAdd() {
        const quickAddButtons = document.querySelectorAll('[data-quick-add]');
        
        quickAddButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const productId = this.dataset.productId;
                const cartIcon = document.querySelector('.cart-icon');
                
                // Анимация иконки
                if (cartIcon) {
                    CartIcons.animateAdd(cartIcon);
                }
                
                // AJAX запрос для добавления в корзину
                this.classList.add('loading');
                
                fetch(this.href, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        CartIcons.updateBadge(data.cart_count);
                        this.classList.remove('loading');
                        
                        // Показываем уведомление
                        CartIcons.showNotification('Товар добавлен в корзину!');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    this.classList.remove('loading');
                });
            });
        });
    }

    // Показ уведомления
    static showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'cart-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                ${message}
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
}

// Вспомогательная функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    CartIcons.initHoverCart();
    CartIcons.initQuickAdd();
});