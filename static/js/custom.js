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
     * Enhance scroll-to-top button with keyboard accessibility and show/hide on scroll
     */
    function enhanceScrollToTop() {
        const scrollUpBtn = document.querySelector('.scroll-up');

        if (scrollUpBtn) {
            // Show/hide based on scroll position
            function toggleScrollButton() {
                if (window.pageYOffset > 300) {
                    scrollUpBtn.classList.add('active');
                } else {
                    scrollUpBtn.classList.remove('active');
                }
            }

            // Check on scroll
            window.addEventListener('scroll', toggleScrollButton);
            // Check on load
            toggleScrollButton();

            // Handle keyboard events (Enter or Space)
            scrollUpBtn.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                }
            });

            // Also handle click (in case main.js doesn't cover it)
            scrollUpBtn.addEventListener('click', function(e) {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }

    /**
     * Skip to main content functionality
     * Focuses the main content area when skip link is activated
     */
    function initSkipLink() {
        const skipLink = document.querySelector('.skip-link');
        const mainContent = document.querySelector('main, [role="main"], #content');

        if (skipLink && mainContent) {
            skipLink.addEventListener('click', function(e) {
                e.preventDefault();

                // Make content focusable if not already
                if (!mainContent.hasAttribute('tabindex')) {
                    mainContent.setAttribute('tabindex', '-1');
                }

                // Focus the main content
                mainContent.focus();

                // Scroll to main content
                mainContent.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            });
        }
    }

    /**
     * Initialize all custom functionality
     */
    function init() {
        handleBrokenImages();
        enhanceFormValidation();
        addLoadingStates();
        initSmoothScroll();
        enhanceScrollToTop();
        initSkipLink();

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
