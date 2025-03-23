document.addEventListener('DOMContentLoaded', function() {
    // Toggle advanced options
    const toggleAdvanced = document.getElementById('toggleAdvanced');
    const advancedFields = document.getElementById('advancedFields');
    
    toggleAdvanced.addEventListener('click', function(e) {
        e.preventDefault();
        const isVisible = advancedFields.style.display === 'block';
        advancedFields.style.display = isVisible ? 'none' : 'block';
        toggleAdvanced.innerHTML = isVisible 
            ? 'Advanced options <i class="fas fa-chevron-down"></i>' 
            : 'Advanced options <i class="fas fa-chevron-up"></i>';
    });
    
    // Form submission
    const shortenForm = document.getElementById('shortenForm');
    const resultDiv = document.getElementById('result');
    const shortUrlInput = document.getElementById('shortUrl');
    const copyButton = document.getElementById('copyButton');
    const statsLink = document.getElementById('statsLink');
    
    shortenForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const url = document.getElementById('url').value;
        const alias = document.getElementById('alias').value;
        const expiration = document.getElementById('expiration').value;
        
        const payload = {
            original_url: url
        };
        
        if (alias) {
            payload.alias = alias;
        }
        
        if (expiration) {
            payload.expires_days = parseInt(expiration);
        }
        
        try {
            const response = await fetch('/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Something went wrong');
            }
            
            const data = await response.json();
            
            // Display result
            shortUrlInput.value = data.short_url;
            statsLink.href = `/stats/${data.short_code}`;
            resultDiv.classList.remove('hidden');
            
            // Update the recent URLs list (would require page reload or DOM update)
        } catch (error) {
            alert(error.message);
        }
    });
    
    // Copy to clipboard
    copyButton.addEventListener('click', function() {
        shortUrlInput.select();
        document.execCommand('copy');
        
        const originalText = copyButton.innerHTML;
        copyButton.innerHTML = '<i class="fas fa-check"></i>';
        
        setTimeout(() => {
            copyButton.innerHTML = originalText;
        }, 2000);
    });
});
