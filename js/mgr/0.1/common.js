document.addEventListener('DOMContentLoaded', () => {
  const root = document.documentElement;
  
  // --- HEADER SELECTORS ---
  const themeSel = document.getElementById('theme-selector');
  const systemMedia = window.matchMedia('(prefers-color-scheme: dark)');
  const masterToggle = document.getElementById('h-mts');
  const headerDropdowns = document.querySelectorAll('.h-md');
  
  // --- FOOTER SELECTORS ---
  const footerNav = document.getElementById('fa');
  const footerCheckboxes = document.querySelectorAll('.f-st');

  // ==========================================
  // 1. ADVANCED MULTI-THEME MANAGEMENT ENGINE
  // ==========================================
  if (themeSel) {
    // Fetch user selection history or default cleanly to operating system preferences
    const savedTheme = localStorage.getItem('theme') || 'system';
    themeSel.value = savedTheme;
    
    /**
     * Translates drop down states directly into active data-theme layout skins
     * @param {string} themeMode - Targets 'system', 'light', 'dark', 'red', or 'eye'
     */
    const applyTheme = (themeMode) => {
      if (themeMode === 'system') {
        // Dynamic evaluation: checks if operating system configuration dictates dark palettes
        const systemPreference = systemMedia.matches ? 'dark' : 'light';
        root.setAttribute('data-theme', systemPreference);
      } else {
        // Directly maps explicit themes ('light', 'dark', 'red', 'eye')
        root.setAttribute('data-theme', themeMode);
      }
    };
    
    // Initialize theme skin matching user's stored criteria on bootstrap execution
    applyTheme(savedTheme);
    
    // Monitor dropdown user select transformations
    themeSel.addEventListener('change', (e) => { 
      const selectedValue = e.target.value;
      localStorage.setItem('theme', selectedValue); 
      applyTheme(selectedValue); 
    });
    
    // Live OS listener tracking window changes while on 'system' mode
    systemMedia.addEventListener('change', () => {
      if (themeSel.value === 'system') {
        applyTheme('system');
      }
    });
  }

  // ==========================================
  // 2. HEADER INTERACTIVE STATE MANAGEMENT
  // ==========================================
  if (masterToggle) {
    masterToggle.addEventListener('change', function() {
      document.body.style.overflow = this.checked ? 'hidden' : '';
    });
  }

  // Exclusive mutual accordion locking logic for Header Dropdowns
  headerDropdowns.forEach(currentInput => {
    currentInput.addEventListener('click', function() {
      if (this.checked) {
        headerDropdowns.forEach(otherInput => {
          if (otherInput !== currentInput && otherInput.checked) {
            otherInput.click();
          }
        });
      }
    });
  });

  const closeAllHeaderMenus = () => {
    if (masterToggle && masterToggle.checked) masterToggle.click();
    headerDropdowns.forEach(checkbox => {
      if (checkbox.checked) checkbox.click();
    });
  };

  // ==========================================
  // 3. GLOBAL CLICK & ESCAPE CONTROLLERS
  // ==========================================
  
  // Close everything instantly when the Escape key is hit
  window.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      closeAllHeaderMenus();
      if (window.innerWidth < 1024) {
        footerCheckboxes.forEach(box => box.checked = false);
      }
    }
  }); 

  // Direct document-wide tap capturing routing matrix
  document.addEventListener('click', (e) => {
    const isMobile = window.innerWidth < 1024;
    
    // --- Header Click Management ---
    // Closes navigation menu drawers if the user touches screen areas outside active headers
    if (!e.target.closest('.hp') && !e.target.closest('.mt') && !e.target.closest('.nw')) {
      closeAllHeaderMenus();
    }

    // --- Footer Click Management (Mobile Responsive Overrides) ---
    if (isMobile) {
      if (footerNav) {
        // Find if a footer layout panel toggle click transaction occurred
        const targetedCheckbox = e.target.closest('.f-mc')?.querySelector('.f-st');
        
        if (targetedCheckbox && targetedCheckbox.checked) {
          // Accordion effect: Close all other footer panels except the active one
          footerCheckboxes.forEach(box => {
            if (box !== targetedCheckbox) {
              box.checked = false;
            }
          });
        }
      } else {
        // Closes all extended footer menus if clicking raw empty space layout targets outside #fa
        footerCheckboxes.forEach(box => box.checked = false);
      }
    }
  });
});
