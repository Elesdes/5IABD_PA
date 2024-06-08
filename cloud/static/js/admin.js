document.addEventListener("DOMContentLoaded", function() {
    // Appel de l'API
    fetch("/api/get_role")
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.querySelectorAll('.admin-only').forEach(element => {
                    element.classList.remove('admin-only');
                });
            }
        })
        .catch(error => {
            console.error('Erreur lors de l\'appel de l\'API:', error);
        });
});
