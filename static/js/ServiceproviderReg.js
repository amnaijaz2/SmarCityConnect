 // Password toggle functionality
 document.querySelector('.toggle-password').addEventListener('click', function() {
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
  
  // File upload preview
  document.getElementById('formFile').addEventListener('change', function(e) {
    const filePreview = document.getElementById('filePreview');
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      reader.onload = function(e) {
        filePreview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        filePreview.style.display = 'block';
      }
      reader.readAsDataURL(this.files[0]);
    }
  });
  
  // Form validation
  (function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();