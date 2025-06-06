document.addEventListener('DOMContentLoaded', function() {
    // Validação do formulário
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Validação de senha
    var password = document.getElementById("nova_senha");
    var confirm_password = document.getElementById("confirmar_senha");

    function validatePassword() {
        if (password.value != confirm_password.value) {
            confirm_password.setCustomValidity("As senhas não coincidem");
        } else {
            confirm_password.setCustomValidity('');
        }
    }

    if (password && confirm_password) {
        password.onchange = validatePassword;
        confirm_password.onkeyup = validatePassword;
    }
});