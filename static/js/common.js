/**
 * Common JavaScript functions for the restaurant management system
 */

// CSRF token handling for AJAX requests
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

// Set up CSRF token for all AJAX requests
function setupCSRFToken() {
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

// Format currency
function formatCurrency(amount) {
    return 'NT$ ' + parseInt(amount).toLocaleString();
}

// Show toast notification
function showToast(message, type = 'success') {
    // Check if Bootstrap 5 toast is available
    if (typeof bootstrap !== 'undefined' && typeof bootstrap.Toast !== 'undefined') {
        // Create toast element
        const toastEl = document.createElement('div');
        toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');

        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        // Add to container
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }

        toastContainer.appendChild(toastEl);

        // Show toast
        const toast = new bootstrap.Toast(toastEl);
        toast.show();

        // Remove after hidden
        toastEl.addEventListener('hidden.bs.toast', function () {
            toastEl.remove();
        });
    } else {
        // Fallback to alert
        alert(message);
    }
}

// Document ready function
document.addEventListener('DOMContentLoaded', function () {
    // Initialize any common functionality here
    console.log('Common JS initialized');
}); 