// Funcionalidades comunes

$(document).ready(function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Tema oscuro
    if (localStorage.getItem('darkMode') === 'true') {
        $('body').addClass('dark-mode');
        $('#theme-toggle i').removeClass('bi-moon').addClass('bi-sun');
    }
    
    $('#theme-toggle').click(function() {
        $('body').toggleClass('dark-mode');
        let isDark = $('body').hasClass('dark-mode');
        localStorage.setItem('darkMode', isDark);
        
        let icon = $(this).find('i');
        if (isDark) {
            icon.removeClass('bi-moon').addClass('bi-sun');
        } else {
            icon.removeClass('bi-sun').addClass('bi-moon');
        }
    });
    
    // Notificaciones
    $('#notification-toggle').click(function() {
        $('.notification-dropdown').toggleClass('show');
    });
    
    // Búsqueda en tiempo real (si existe el campo)
    $('#search-input').on('keyup', function() {
        let query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: '/api/buscar',
                method: 'GET',
                data: { q: query },
                success: function(data) {
                    // Mostrar resultados
                    console.log(data);
                }
            });
        }
    });
});

// Función para mostrar mensajes flash temporales
function showFlashMessage(message, type = 'info') {
    let alertDiv = $(`<div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>`);
    
    $('.flash-messages').append(alertDiv);
    
    setTimeout(function() {
        alertDiv.alert('close');
    }, 5000);
}

// Función para validar formularios
function validateForm(formId) {
    let valid = true;
    $(`#${formId} input[required], #${formId} select[required], #${formId} textarea[required]`).each(function() {
        if (!$(this).val()) {
            $(this).addClass('is-invalid');
            valid = false;
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    return valid;
}

// Función para copiar texto al portapapeles
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showFlashMessage('Texto copiado al portapapeles', 'success');
    }, function() {
        showFlashMessage('Error al copiar el texto', 'danger');
    });
}

// Función para compartir en redes sociales
function shareOnSocial(platform, url, title) {
    let shareUrl;
    
    switch(platform) {
        case 'facebook':
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
            break;
        case 'twitter':
            shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;
            break;
        case 'linkedin':
            shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
            break;
        case 'whatsapp':
            shareUrl = `https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`;
            break;
    }
    
    if (shareUrl) {
        window.open(shareUrl, '_blank', 'width=600,height=400');
    }
}

// Función para calcular progreso
function calculateProgress(completed, total) {
    return Math.round((completed / total) * 100);
}

// Función para actualizar barra de progreso
function updateProgressBar(elementId, percentage) {
    $(`#${elementId}`).css('width', percentage + '%').attr('aria-valuenow', percentage);
    $(`#${elementId} .progress-text`).text(percentage + '%');
}

// Función para manejar errores de AJAX
$(document).ajaxError(function(event, jqxhr, settings, thrownError) {
    console.error('Error AJAX:', thrownError);
    showFlashMessage('Error en la conexión. Por favor, intenta de nuevo.', 'danger');
});
