document.addEventListener('DOMContentLoaded', (event) => {
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');
    const passwordSuccess = document.getElementById('passwordSuccess');
    const submitBtn = document.getElementById('submitBtn');

    function validatePassword() {
        if (passwordInput.value.length < 8) {
            passwordError.style.display = 'inline';
            passwordSuccess.style.display = 'none';
            submitBtn.disabled = true;
        } else {
            passwordError.style.display = 'none';
            passwordSuccess.style.display = 'inline';
            submitBtn.disabled = false;
        }
    }

    passwordInput.addEventListener('blur', validatePassword);
    passwordInput.addEventListener('focus', (event) => {
        passwordError.style.display = 'none';
        passwordSuccess.style.display = 'none';
    });

    passwordInput.addEventListener('input', validatePassword);

    // Initial check in case the form is pre-filled or the user pastes a password
    validatePassword();
});