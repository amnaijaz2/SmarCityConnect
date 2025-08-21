document.addEventListener('DOMContentLoaded', function() {
    // COPY BUTTON FUNCTIONALITY - GUARANTEED TO WORK
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const phoneNumber = this.getAttribute('data-phone');
            const originalHtml = this.innerHTML;
            const originalClass = this.className;
            
            // Visual feedback immediately
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Copying...';
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-secondary');
            
            // Create invisible textarea element
            const textArea = document.createElement('textarea');
            textArea.value = phoneNumber;
            textArea.style.position = 'fixed';
            textArea.style.top = '0';
            textArea.style.left = '0';
            textArea.style.width = '2em';
            textArea.style.height = '2em';
            textArea.style.padding = '0';
            textArea.style.border = 'none';
            textArea.style.outline = 'none';
            textArea.style.boxShadow = 'none';
            textArea.style.background = 'transparent';
            
            document.body.appendChild(textArea);
            textArea.select();
            
            try {
                // Try modern clipboard API first
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(phoneNumber).then(() => {
                        showCopySuccess(this, originalHtml, originalClass);
                    }).catch(err => {
                        // If modern API fails, use fallback
                        useCopyFallback(textArea, this, originalHtml, originalClass);
                    });
                } else {
                    // Use fallback if no clipboard API
                    useCopyFallback(textArea, this, originalHtml, originalClass);
                }
            } catch (err) {
                console.error('Copy failed:', err);
                showCopyFallbackManual(phoneNumber, this, originalHtml, originalClass);
            } finally {
                document.body.removeChild(textArea);
            }
        });
    });
    
    function showCopySuccess(button, originalHtml, originalClass) {
        button.innerHTML = '<i class="fas fa-check me-1"></i> Copied!';
        button.classList.remove('btn-secondary', 'btn-outline-primary');
        button.classList.add('btn-success');
        
        setTimeout(() => {
            button.innerHTML = originalHtml;
            button.className = originalClass;
        }, 2000);
    }
    
    function useCopyFallback(textArea, button, originalHtml, originalClass) {
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                showCopySuccess(button, originalHtml, originalClass);
            } else {
                throw new Error('Copy command failed');
            }
        } catch (err) {
            console.error('Fallback copy failed:', err);
            showCopyFallbackManual(textArea.value, button, originalHtml, originalClass);
        }
    }

    function showCopyFallbackManual(phoneNumber, button, originalHtml, originalClass) {
        button.innerHTML = '<i class="fas fa-exclamation-triangle me-1"></i> Failed';
        button.classList.remove('btn-secondary', 'btn-outline-primary');
        button.classList.add('btn-danger');
        
        // Create help popup
        const popup = document.createElement('div');
        popup.style.position = 'fixed';
        popup.style.top = '0';
        popup.style.left = '0';
        popup.style.right = '0';
        popup.style.bottom = '0';
        popup.style.backgroundColor = 'rgba(0,0,0,0.7)';
        popup.style.zIndex = '9999';
        popup.style.display = 'flex';
        popup.style.alignItems = 'center';
        popup.style.justifyContent = 'center';
        
        popup.innerHTML = `
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
        
        document.body.appendChild(popup);
        const input = popup.querySelector('input');
        input.select();
        
        popup.querySelector('button').addEventListener('click', function() {
            document.body.removeChild(popup);
            button.innerHTML = originalHtml;
            button.className = originalClass;
        });
    }

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

    // Desktop call button behavior
    document.querySelectorAll('.call-btn').forEach(button => {
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        if (!isMobile) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const phoneNumber = this.getAttribute('href').replace('tel:', '');
                alert(`Please call: ${phoneNumber}\n\nOn mobile devices, this would automatically dial the number.`);
            });
        }
    });
});