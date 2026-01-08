/**
 * Theme Toggle for Lottery Lab
 * 
 * Handles switching between dark and light themes.
 * Persists user preference in localStorage.
 * Respects system preference on first visit.
 */

(function() {
    'use strict';

    const STORAGE_KEY = 'lottery-lab-theme';
    const DARK = 'dark';
    const LIGHT = 'light';

    /**
     * Get the user's preferred theme
     * Priority: localStorage > system preference > default (dark)
     */
    function getPreferredTheme() {
        // Check localStorage first
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored === DARK || stored === LIGHT) {
            return stored;
        }

        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
            return LIGHT;
        }

        // Default to dark
        return DARK;
    }

    /**
     * Apply theme to document
     */
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(STORAGE_KEY, theme);
        
        // Update toggle button icons if exists
        updateToggleButton(theme);
    }

    /**
     * Toggle between themes
     */
    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme') || DARK;
        const next = current === DARK ? LIGHT : DARK;
        applyTheme(next);
    }

    /**
     * Update toggle button appearance
     */
    function updateToggleButton(theme) {
        const toggle = document.getElementById('theme-toggle');
        if (!toggle) return;

        const sunIcon = toggle.querySelector('.icon-sun');
        const moonIcon = toggle.querySelector('.icon-moon');

        if (sunIcon && moonIcon) {
            if (theme === DARK) {
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
            } else {
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
            }
        }

        // Update title/aria-label
        toggle.setAttribute('title', theme === DARK ? 'Switch to light mode' : 'Switch to dark mode');
        toggle.setAttribute('aria-label', theme === DARK ? 'Switch to light mode' : 'Switch to dark mode');
    }

    /**
     * Initialize theme system
     */
    function init() {
        // Apply theme immediately (before DOMContentLoaded to prevent flash)
        const theme = getPreferredTheme();
        applyTheme(theme);

        // Set up toggle button when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupToggle);
        } else {
            setupToggle();
        }

        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
                // Only auto-switch if user hasn't manually set preference
                if (!localStorage.getItem(STORAGE_KEY)) {
                    applyTheme(e.matches ? LIGHT : DARK);
                }
            });
        }
    }

    /**
     * Set up toggle button click handler
     */
    function setupToggle() {
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            toggle.addEventListener('click', toggleTheme);
            updateToggleButton(getPreferredTheme());
        }
    }

    // Expose to global scope for manual usage
    window.LotteryLabTheme = {
        toggle: toggleTheme,
        set: applyTheme,
        get: getPreferredTheme
    };

    // Initialize
    init();
})();

