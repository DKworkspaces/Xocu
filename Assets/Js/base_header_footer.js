/**
 * Global UI Layer Orchestrator
 * Handles Header drawers, responsive navigation grids, and theme management
 */
document.addEventListener('DOMContentLoaded', () => {
  // Elements Selection Matrix
  const menuToggle = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu-wrapper');
  const dropdownTriggers = document.querySelectorAll('.dropdown-trigger');
  const modeSelect = document.querySelector('.mode-select');
  const footerAccordion = document.getElementById("footer-nav-accordion");

  // ==========================================================================
  // HELPER FUNCTIONS (Focus Management & State Cleaners)
  // ==========================================================================
  
  /**
   * Toggles keyboard focus indicators inside the mobile slide drawer
   * Fixes focus leaks behind active application viewports
   */
  function toggleDrawerFocus(isOpen) {
    if (!navMenu) return;
    const focusableElements = navMenu.querySelectorAll('a, button, input, select');
    focusableElements.forEach(el => {
      if (window.innerWidth <= 1024) {
        isOpen ? el.removeAttribute('tabindex') : el.setAttribute('tabindex', '-1');
      } else {
        el.removeAttribute('tabindex');
      }
    });
  }

  /**
   * Resets and cleans active navigational state structures
   * Syncs custom layout open tracking hooks
   */
  function closeAllMenus() {
    document.querySelectorAll('.nav-links > li').forEach(li => {
      li.classList.remove('is-open');
      const trigger = li.querySelector('.dropdown-trigger');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
    });
  }

  // ==========================================================================
  // SUB-MODULE 1: HEADER MOBILE DRAWER LAYER
  // ==========================================================================
  if (menuToggle && navMenu) {
    // Initial runtime focus pipeline setup pass
    toggleDrawerFocus(false);

    menuToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = menuToggle.classList.toggle('is-active');
      navMenu.classList.toggle('is-active');
      menuToggle.setAttribute('aria-expanded', isOpen);
      toggleDrawerFocus(isOpen);
    });
  }

  // ==========================================================================
  // SUB-MODULE 2: HEADER INTERACTIVE DROPDOWNS & MEGAMENUS
  // ==========================================================================
  dropdownTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const parentLi = trigger.parentElement;
      const isOpen = parentLi.classList.contains('is-open');

      // Closes neighboring active lists to enforce single-open logic flow
      const siblingContainer = trigger.closest('.nav-links');
      if (siblingContainer) {
        siblingContainer.querySelectorAll('li').forEach(li => {
          if (li !== parentLi) {
            li.classList.remove('is-open');
            const innerBtn = li.querySelector('.dropdown-trigger');
            if (innerBtn) innerBtn.setAttribute('aria-expanded', 'false');
          }
        });
      }

      parentLi.classList.toggle('is-open', !isOpen);
      trigger.setAttribute('aria-expanded', !isOpen);
    });
  });

  // ==========================================================================
  // SUB-MODULE 3: FOOTER COLLAPSIBLE ACCORDION PATTERN
  // ==========================================================================
  if (footerAccordion) {
    footerAccordion.addEventListener("click", (event) => {
      // Escape processing block on desktop platforms
      if (window.innerWidth >= 1024) return;

      const trigger = event.target.closest(".mega-menu-trigger");
      if (!trigger) return;

      const parentColumn = trigger.parentElement;
      const isExpanded = trigger.getAttribute("aria-expanded") === "true";

      trigger.setAttribute("aria-expanded", !isExpanded);
      parentColumn.classList.toggle('is-active');
    });
  }

  // ==========================================================================
  // SUB-MODULE 4: GLOBAL CANVAS BACKGROUND CLICK OVERLAYS
  // ==========================================================================
  document.addEventListener('click', (e) => {
    if (window.innerWidth > 1024) {
      closeAllMenus();
    }
    
    if (window.innerWidth <= 1024 && navMenu && menuToggle) {
      if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
        menuToggle.classList.remove('is-active');
        navMenu.classList.remove('is-active');
        menuToggle.setAttribute('aria-expanded', 'false');
        closeAllMenus();
        toggleDrawerFocus(false);
      }
    }
  });

  // ==========================================================================
  // SUB-MODULE 5: VIEWPORT ENVIRONMENT RE-EVALUATION PIPELINE
  // ==========================================================================
  window.addEventListener('resize', () => {
    if (window.innerWidth > 1024) {
      if (menuToggle && navMenu) {
        menuToggle.classList.remove('is-active');
        navMenu.classList.remove('is-active');
        menuToggle.setAttribute('aria-expanded', 'false');
      }
      closeAllMenus();
      toggleDrawerFocus(true);
      
      // Cleanup footer accessibility flags when scaling up to desktop systems
      if (footerAccordion) {
        footerAccordion.querySelectorAll('.mega-menu-trigger').forEach(trigger => {
          trigger.removeAttribute('aria-expanded');
          trigger.parentElement.classList.remove('is-active');
        });
      }
    } else {
      toggleDrawerFocus(false);
      
      // Re-apply navigation frame properties when scaling back down to mobile devices
      if (footerAccordion) {
        footerAccordion.querySelectorAll('.mega-menu-trigger').forEach(trigger => {
          const isActive = trigger.parentElement.classList.contains('is-active');
          trigger.setAttribute('aria-expanded', isActive ? 'true' : 'false');
        });
      }
    }
  });

  // ==========================================================================
  // SUB-MODULE 6: DATA-THEME STATE SYSTEM MATRIX
  // ==========================================================================
  if (modeSelect) {
    const cachedTheme = localStorage.getItem('theme') || 'system';
    modeSelect.value = cachedTheme;
    applyTheme(cachedTheme);

    modeSelect.addEventListener('change', (e) => {
      const selectedTheme = e.target.value;
      localStorage.setItem('theme', selectedTheme);
      applyTheme(selectedTheme);
    });
  }

  function applyTheme(theme) {
    if (theme === 'system') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    } else {
      document.documentElement.setAttribute('data-theme', theme);
    }
  }

  // Monitor real-time OS-level configuration changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (modeSelect && modeSelect.value === 'system') {
      applyTheme('system');
    }
  });
});
  
