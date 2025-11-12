/**
 * Custom JavaScript for Far Out Corporation
 *
 * Project-specific functionality and enhancements
 */

(function() {
    'use strict';

    /**
     * Handle broken images (especially for lazy-loaded ship images from API)
     */
    function handleBrokenImages() {
        const images = document.querySelectorAll('img[loading="lazy"]');

        images.forEach(img => {
            img.addEventListener('error', function() {
                // Only replace once to avoid infinite loop
                if (!this.classList.contains('broken')) {
                    this.classList.add('broken');
                    // Use a data attribute or fall back to placeholder
                    const placeholder = this.dataset.placeholder || '/static/img/placeholder-ship.jpg';
                    this.src = placeholder;
                    this.alt = 'Image not available';
                }
            });
        });
    }

    /**
     * Enhance form validation with better UX
     */
    function enhanceFormValidation() {
        const forms = document.querySelectorAll('form[novalidate]');

        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    /**
     * Add loading state to buttons on form submit
     */
    function addLoadingStates() {
        const forms = document.querySelectorAll('form');

        forms.forEach(form => {
            form.addEventListener('submit', function() {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn && !submitBtn.disabled) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';

                    // Re-enable after 5 seconds as failsafe
                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalText;
                    }, 5000);
                }
            });
        });
    }

    /**
     * Smooth scroll for anchor links
     */
    function initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]:not([href="#"])');

        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href').substring(1);
                const target = document.getElementById(targetId);

                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });

                    // Update URL without jumping
                    if (history.pushState) {
                        history.pushState(null, null, `#${targetId}`);
                    }
                }
            });
        });
    }

    /**
     * Initialize all custom functionality
     */
    function init() {
        handleBrokenImages();
        enhanceFormValidation();
        addLoadingStates();
        initSmoothScroll();

        // Log initialization for debugging
        if (window.console && console.log) {
            console.log('Far Out Custom JS initialized');
        }
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM is already ready
        init();
    }

})();
