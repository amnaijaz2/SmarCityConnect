document.addEventListener('DOMContentLoaded', function() {
    // ULTRA-RELIABLE COPY FUNCTIONALITY
    document.body.addEventListener('click', async function(event) {
        const copyBtn = event.target.closest('.copy-btn');
        if (!copyBtn) return;

        const phoneNumber = copyBtn.getAttribute('data-phone');
        const originalContent = copyBtn.innerHTML;
        const originalClasses = copyBtn.className;

        // Visual feedback immediately
        copyBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Copying...';
        copyBtn.classList.remove('btn-outline-primary');
        copyBtn.classList.add('btn-secondary');
        
        try {
            // Method 1: Modern Clipboard API (async/await)
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(phoneNumber);
                showSuccess();
                return;
            }

            // Method 2: execCommand fallback
            const textArea = document.createElement('textarea');
            textArea.value = phoneNumber;
            textArea.style.position = 'fixed';
            textArea.style.top = '-999px';
            textArea.style.left = '-999px';
            document.body.appendChild(textArea);
            textArea.select();

            if (document.execCommand('copy')) {
                showSuccess();
                document.body.removeChild(textArea);
                return;
            }

            // Method 3: Selectable div fallback for mobile
            const selectableDiv = document.createElement('div');
            selectableDiv.contentEditable = true;
            selectableDiv.textContent = phoneNumber;
            selectableDiv.style.position = 'fixed';
            selectableDiv.style.top = '-999px';
            document.body.appendChild(selectableDiv);

            const range = document.createRange();
            range.selectNode(selectableDiv);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);

            if (document.execCommand('copy')) {
                showSuccess();
                document.body.removeChild(selectableDiv);
                return;
            }

            // If all methods fail
            throw new Error('All copy methods failed');

        } catch (err) {
            console.error('Copy failed:', err);
            showFallback();
        }

        function showSuccess() {
            copyBtn.innerHTML = '<i class="fas fa-check me-1"></i> Copied!';
            copyBtn.classList.remove('btn-secondary');
            copyBtn.classList.add('btn-success');
            
            setTimeout(() => {
                copyBtn.innerHTML = originalContent;
                copyBtn.className = originalClasses;
            }, 2000);
        }

        function showFallback() {
            copyBtn.innerHTML = '<i class="fas fa-exclamation-triangle me-1"></i> Click to Copy';
            copyBtn.classList.remove('btn-secondary');
            copyBtn.classList.add('btn-warning');
            
            // Create a modal-like prompt
            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.right = '0';
            modal.style.bottom = '0';
            modal.style.backgroundColor = 'rgba(0,0,0,0.7)';
            modal.style.zIndex = '9999';
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            
            modal.innerHTML = `
                <div style="background: white; padding: 20px; border-radius: 5px; max-width: 90%;">
                    <h5 style="margin-top: 0">Manual Copy Required</h5>
                    <p>Please copy this number:</p>
                    <input type="text" value="${phoneNumber}" readonly 
                           style="width: 100%; padding: 8px; font-size: 16px; text-align: center; margin-bottom: 15px;">
                    <button style="padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 4px;">
                        I've Copied It
                    </button>
                </div>
            `;
            
            document.body.appendChild(modal);
            const input = modal.querySelector('input');
            input.select();
            
            modal.querySelector('button').addEventListener('click', function() {
                document.body.removeChild(modal);
                copyBtn.innerHTML = originalContent;
                copyBtn.className = originalClasses;
            });
        }
    });

    // Initialize carousel if available
    if (typeof bootstrap !== 'undefined') {
        const carouselEl = document.getElementById('serviceCarousel');
        if (carouselEl) {
            new bootstrap.Carousel(carouselEl, {
                interval: 5000,
                pause: 'hover'
            });
        }
    }
});