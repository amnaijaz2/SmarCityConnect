document.addEventListener('DOMContentLoaded', function() {
        const loginForm = document.getElementById('loginForm');
        
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                const username = document.getElementById('username');
                const password = document.getElementById('password');
                
                // Simple validation - just check if fields are not empty
                if (username.value.trim() === '' || password.value.trim() === '') {
                    e.preventDefault();
                    if (username.value.trim() === '') {
                        username.focus();
                    } else {
                        password.focus();
                    }
                }
            });
            
            // Add focus effects
            const inputs = document.querySelectorAll('.form-control');
            inputs.forEach(input => {
                input.addEventListener('focus', function() {
                    this.parentElement.querySelector('.input-icon').style.color = '#3498db';
                    this.parentElement.querySelector('.input-icon').style.transform = 'scale(1.1)';
                });
                
                input.addEventListener('blur', function() {
                    this.parentElement.querySelector('.input-icon').style.color = '#7f8c8d';
                    this.parentElement.querySelector('.input-icon').style.transform = 'scale(1)';
                });
            });
        }
    });