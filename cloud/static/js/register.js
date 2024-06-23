document.addEventListener('DOMContentLoaded', (event) => {
    const passwordInput = document.getElementById('password');
    const passwordSuccess = document.getElementById('passwordSuccess');
    const submitBtn = document.getElementById('submitBtn');
    const passwordErrorLength = document.getElementById('passwordErrorLength');
    const passwordErrorUppercase = document.getElementById('passwordErrorUppercase');
    const passwordErrorLowercase = document.getElementById('passwordErrorLowercase');
    const passwordErrorNumber = document.getElementById('passwordErrorNumber');
    const passwordErrorSpecial = document.getElementById('passwordErrorSpecial');

    function validatePassword() {
        const password = passwordInput.value;
        let isValid = true;

        if (password.length < 8) {
            passwordErrorLength.style.display = 'block';
            isValid = false;
        } else {
            passwordErrorLength.style.display = 'none';
        }

        if (!/[A-Z]/.test(password)) {
            passwordErrorUppercase.style.display = 'block';
            isValid = false;
        } else {
            passwordErrorUppercase.style.display = 'none';
        }

        if (!/[a-z]/.test(password)) {
            passwordErrorLowercase.style.display = 'block';
            isValid = false;
        } else {
            passwordErrorLowercase.style.display = 'none';
        }

        if (!/[0-9]/.test(password)) {
            passwordErrorNumber.style.display = 'block';
            isValid = false;
        } else {
            passwordErrorNumber.style.display = 'none';
        }

        if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            passwordErrorSpecial.style.display = 'block';
            isValid = false;
        } else {
            passwordErrorSpecial.style.display = 'none';
        }

        if (isValid) {
            passwordSuccess.style.display = 'block';
            submitBtn.disabled = false;
        } else {
            passwordSuccess.style.display = 'none';
            submitBtn.disabled = true;
        }
    }

    passwordInput.addEventListener('blur', validatePassword);
    /*
    passwordInput.addEventListener('focus', (event) => {
        passwordSuccess.style.display = 'none';
        passwordErrorLength.style.display = 'none';
        passwordErrorUppercase.style.display = 'none';
        passwordErrorLowercase.style.display = 'none';
        passwordErrorNumber.style.display = 'none';
        passwordErrorSpecial.style.display = 'none';
    });
    */

    passwordInput.addEventListener('input', validatePassword);

    // Initial check in case the form is pre-filled or the user pastes a password
    validatePassword();
});