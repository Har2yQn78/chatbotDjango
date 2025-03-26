function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type}`;
    
    const icon = type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-circle-fill';
    
    toast.innerHTML = `
        <div class="toast-icon">
            <i class="bi ${icon}"></i>
        </div>
        <div class="toast-content">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, 5000);
}

document.addEventListener('submit', function(e) {
    showLoading();
})
document.addEventListener('DOMContentLoaded', function() {
    const syncButton = document.getElementById('syncButton');
    if (syncButton) {
        syncButton.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<i class="bi bi-arrow-repeat me-2 spin"></i>Syncing...';
            
            showLoading();
            
            const formData = new FormData();
            formData.append('sync_rag', 'true');
            formData.append('csrfmiddlewaretoken', csrfToken);
            
            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                showToast(data.message, data.success ? 'success' : 'error');
                this.disabled = false;
                this.innerHTML = originalText;
            })
            .catch(error => {
                console.error('Error:', error);
                hideLoading();
                showToast('An error occurred during sync', 'error');
                this.disabled = false;
                this.innerHTML = originalText;
            });
        });
    }
});

$(document).ajaxStart(function() {
    showLoading();
});

$(document).ajaxStop(function() {
    hideLoading();
});