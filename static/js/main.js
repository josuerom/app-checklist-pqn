// ===================================
// CONSTANTES Y CONFIGURACIÓN
// ===================================
const CONFIG = {
    animationDuration: 300,
    toastDuration: 5000,
    debounceDelay: 300
};

// ===================================
// INICIALIZACIÓN
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 App iniciada');
    
    // Inicializar módulos
    initializeTooltips();
    initializeAnimations();
    initializeFormValidations();
    initializeScrollEffects();
    initializeKeyboardShortcuts();
    
    // Log de versión
    console.log('📦 Versión: 1.1.0');
    console.log('👨‍💻 Desarrollado por: Josué Romero');
});

// ===================================
// TOOLTIPS
// ===================================
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggerList.forEach(element => {
        element.addEventListener('mouseenter', function() {
            showTooltip(this);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip(this);
        });
    });
}

function showTooltip(element) {
    const text = element.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    
    tooltip.className = 'tooltip-custom';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        z-index: 9999;
        pointer-events: none;
        white-space: nowrap;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
    
    element._tooltip = tooltip;
}

function hideTooltip(element) {
    if (element._tooltip) {
        element._tooltip.remove();
        delete element._tooltip;
    }
}

// ===================================
// ANIMACIONES AL SCROLL
// ===================================
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// ===================================
// VALIDACIÓN DE FORMULARIOS
// ===================================
function initializeFormValidations() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showNotification('Por favor, completa todos los campos requeridos', 'warning');
            }
        });
        
        // Validación en tiempo real
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', debounce(function() {
                validateField(this);
            }, CONFIG.debounceDelay));
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // Validar campo requerido
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'Este campo es obligatorio';
    }
    
    // Validar email
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Email inválido';
        }
    }
    
    // Validar longitud mínima
    if (field.hasAttribute('minlength') && value) {
        const minLength = parseInt(field.getAttribute('minlength'));
        if (value.length < minLength) {
            isValid = false;
            errorMessage = `Mínimo ${minLength} caracteres`;
        }
    }
    
    // Aplicar clases de validación
    if (isValid) {
        field.classList.remove('border-red-500');
        field.classList.add('border-green-500');
        removeFieldError(field);
    } else {
        field.classList.remove('border-green-500');
        field.classList.add('border-red-500');
        showFieldError(field, errorMessage);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    removeFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error text-red-600 text-sm mt-1';
    errorDiv.textContent = message;
    errorDiv.setAttribute('data-error-for', field.id || field.name);
    
    field.parentNode.appendChild(errorDiv);
}

function removeFieldError(field) {
    const errorId = field.id || field.name;
    const existingError = field.parentNode.querySelector(`[data-error-for="${errorId}"]`);
    
    if (existingError) {
        existingError.remove();
    }
}

// ===================================
// NOTIFICACIONES (TOAST)
// ===================================
function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    
    const bgColors = {
        success: 'bg-green-500',
        warning: 'bg-yellow-500',
        error: 'bg-red-500',
        info: 'bg-blue-500'
    };
    
    const icons = {
        success: 'bi-check-circle-fill',
        warning: 'bi-exclamation-triangle-fill',
        error: 'bi-x-circle-fill',
        info: 'bi-info-circle-fill'
    };
    
    toast.className = `fixed top-4 right-4 ${bgColors[type]} text-white px-6 py-4 rounded-lg shadow-2xl z-50 flex items-center gap-3 animate__animated animate__slideInRight`;
    toast.innerHTML = `
        <i class="bi ${icons[type]} text-2xl"></i>
        <span class="font-semibold">${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-4 hover:bg-white hover:bg-opacity-20 rounded p-1">
            <i class="bi bi-x-lg"></i>
        </button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('animate__slideOutRight');
        setTimeout(() => toast.remove(), 300);
    }, CONFIG.toastDuration);
}

// ===================================
// EFECTOS DE SCROLL
// ===================================
function initializeScrollEffects() {
    let lastScrollTop = 0;
    const header = document.querySelector('.fixed-header');
    
    if (header) {
        window.addEventListener('scroll', debounce(function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop) {
                // Scroll hacia abajo
                header.style.transform = 'translateY(-100%)';
            } else {
                // Scroll hacia arriba
                header.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop;
        }, 100));
    }
    
    // Botón "Volver arriba"
    const backToTopBtn = createBackToTopButton();
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'flex';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
}

function createBackToTopButton() {
    const btn = document.createElement('button');
    btn.innerHTML = '<i class="bi bi-arrow-up text-2xl"></i>';
    btn.className = 'fixed bottom-8 right-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white w-14 h-14 rounded-full shadow-2xl hover:scale-110 transition-transform duration-300 z-50 items-center justify-center';
    btn.style.display = 'none';
    
    btn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    document.body.appendChild(btn);
    return btn;
}

// ===================================
// ATAJOS DE TECLADO
// ===================================
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl + K: Focus en búsqueda (si existe)
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) searchInput.focus();
        }
        
        // ESC: Cerrar modales o limpiar búsqueda
        if (e.key === 'Escape') {
            const activeModals = document.querySelectorAll('.modal.active');
            activeModals.forEach(modal => modal.classList.remove('active'));
            
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) searchInput.value = '';
        }
    });
}

// ===================================
// UTILIDADES
// ===================================

/**
 * Debounce function para optimizar eventos
 */
function debounce(func, wait) {
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

/**
 * Copiar texto al portapapeles
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Texto copiado al portapapeles', 'success');
        }).catch(err => {
            console.error('Error al copiar:', err);
            showNotification('Error al copiar texto', 'error');
        });
    } else {
        // Fallback para navegadores antiguos
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        
        try {
            document.execCommand('copy');
            showNotification('Texto copiado al portapapeles', 'success');
        } catch (err) {
            console.error('Error al copiar:', err);
            showNotification('Error al copiar texto', 'error');
        }
        
        document.body.removeChild(textarea);
    }
}

/**
 * Formatear fecha
 */
function formatDate(date, format = 'DD/MM/YYYY') {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    
    return format
        .replace('DD', day)
        .replace('MM', month)
        .replace('YYYY', year);
}

/**
 * Detectar dispositivo móvil
 */
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/**
 * Cargar script dinámicamente
 */
function loadScript(src, callback) {
    const script = document.createElement('script');
    script.src = src;
    script.onload = callback;
    document.head.appendChild(script);
}

// ===================================
// EXPORTS (para uso en otros scripts)
// ===================================
window.AppUtils = {
    showNotification,
    copyToClipboard,
    formatDate,
    debounce,
    isMobile,
    loadScript
};

// Log de inicialización
console.log('✅ Scripts principales cargados correctamente');