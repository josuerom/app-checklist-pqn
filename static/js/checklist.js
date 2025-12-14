const totalPreguntas = document.querySelectorAll('.question-card').length;
let preguntasCompletadas = new Set();

/**
 * Inicialización
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeClickableCards();
    initializeAutoRedirect();
});

/**
 * Hacer las tarjetas clickeables para selección cíclica
 */
function initializeClickableCards() {
    document.querySelectorAll('.question-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Si se hizo clic en un checkbox, no hacer nada
            if (e.target.closest('.checkbox-option')) return;
            
            const cbOK = card.querySelector('input[value="OK"]');
            const cbNA = card.querySelector('input[value="N/A"]');
            const cbPD = card.querySelector('input[value="PD"]');
            
            // Ciclo: sin seleccionar → OK → N/A → PD → sin seleccionar
            if (!cbOK.checked && !cbNA.checked && !cbPD.checked) {
                cbOK.click();
            } else if (cbOK.checked) {
                cbNA.click();
            } else if (cbNA.checked) {
                cbPD.click();
            } else if (cbPD.checked) {
                cbPD.checked = false;
                handleCheckbox(cbPD, card.dataset.question);
            }
        });
    });
}

/**
 * Manejar cambio de checkbox
 */
function handleCheckbox(checkbox, questionNum) {
    const card = document.querySelector(`[data-question="${questionNum}"]`);
    const checkboxes = card.querySelectorAll('input[type="checkbox"]');
    const labels = card.querySelectorAll('.checkbox-option');
    
    // Desmarcar otros checkboxes
    checkboxes.forEach(cb => {
        if (cb !== checkbox) cb.checked = false;
    });
    
    // Limpiar clases de estilo
    labels.forEach(label => {
        label.classList.remove('checked-ok', 'checked-na', 'checked-pd');
    });
    
    // Aplicar estilos según selección
    if (checkbox.checked) {
        const label = checkbox.closest('.checkbox-option');
        const type = label.getAttribute('data-type');
        
        if (type === 'ok') label.classList.add('checked-ok');
        if (type === 'na') label.classList.add('checked-na');
        if (type === 'pd') label.classList.add('checked-pd');
        
        preguntasCompletadas.add(questionNum);
        card.classList.add('completed');
    } else {
        preguntasCompletadas.delete(questionNum);
        card.classList.remove('completed');
    }
    
    updateProgress();
}

/**
 * Actualizar barra de progreso
 */
function updateProgress() {
    const completadas = preguntasCompletadas.size;
    const porcentaje = Math.round((completadas / totalPreguntas) * 100);
    
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const submitBtn = document.getElementById('submitBtn');
    const completionBadge = document.getElementById('completionBadge');
    
    // Actualizar barra
    progressBar.style.width = porcentaje + '%';
    progressBar.textContent = porcentaje + '%';
    
    // Actualizar texto
    progressText.innerHTML = `<strong>${completadas}</strong> de <strong>${totalPreguntas}</strong> preguntas completadas`;
    
    // Habilitar/deshabilitar botón
    submitBtn.disabled = completadas !== totalPreguntas;
    
    // Mostrar badge de completado
    if (completadas === totalPreguntas) {
        completionBadge.classList.remove('hidden');
        submitBtn.classList.add('animate__animated', 'animate__pulse');
    } else {
        completionBadge.classList.add('hidden');
        submitBtn.classList.remove('animate__animated', 'animate__pulse');
    }
}

/**
 * Auto-redirección después de guardar
 */
function initializeAutoRedirect() {
    const alertEl = document.getElementById('successAlert');
    
    if (alertEl) {
        setTimeout(() => {
            alertEl.classList.add('animate__animated', 'animate__fadeOut');
            
            setTimeout(() => {
                window.location.href = '/home';
            }, 1000);
        }, 10000); // 10 segundos
    }
}

/**
 * Validación antes de enviar formulario
 */
document.getElementById('checklistForm')?.addEventListener('submit', function(e) {
    if (preguntasCompletadas.size !== totalPreguntas) {
        e.preventDefault();
        alert('Por favor, completa todas las preguntas antes de continuar');
        return false;
    }
    
    // Mostrar loader
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.innerHTML = '<i class="bi bi-hourglass-split mr-2 animate-spin"></i>Guardando...';
    submitBtn.disabled = true;
});

/**
 * Scroll suave al hacer clic en una tarjeta
 */
document.querySelectorAll('.question-card').forEach(card => {
    card.addEventListener('click', function() {
        this.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    });
});