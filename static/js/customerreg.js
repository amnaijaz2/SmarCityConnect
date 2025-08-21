         // Password toggle functionality
         document.querySelector('.pw-toggle').addEventListener('click', function() {
            const passwordInput = document.querySelector('#password');
            const icon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
              passwordInput.type = 'text';
              icon.classList.remove('fa-eye');
              icon.classList.add('fa-eye-slash');
            } else {
              passwordInput.type = 'password';
              icon.classList.remove('fa-eye-slash');
              icon.classList.add('fa-eye');
            }
          });
          
          // Form toggle animation
          const toggleBtns = document.querySelectorAll('.toggle-btn');
          const toggleAfter = document.querySelector('.form-toggle::after');
          
          toggleBtns.forEach(btn => {
            btn.addEventListener('click', function() {
              if (!this.classList.contains('active')) {
                document.querySelector('.toggle-btn.active').classList.remove('active');
                this.classList.add('active');
              }
            });
          });