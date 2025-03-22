document.addEventListener('DOMContentLoaded', function() {

    console.log('RAG UI initialized');

    const queryForm = document.getElementById('query-form');
    if (queryForm) {
        queryForm.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            submitButton.disabled = true;
            
            setTimeout(function() {
                submitButton.innerHTML = 'Submit Query';
                submitButton.disabled = false;
            }, 30000);
        });
    }
});