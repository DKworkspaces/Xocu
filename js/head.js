document.addEventListener('DOMContentLoaded', () => {
  const root = document.documentElement;
  const themeSel = document.getElementById('theme-selector');
  const systemMedia = window.matchMedia('(prefers-color-scheme: dark)');
  const masterToggle = document.getElementById('menu-toggle-state');
  const dropdowns = document.querySelectorAll('.menu-dropdown');

  if (!themeSel) return;

  // 1. Theme Configuration Engine
  themeSel.value = localStorage.getItem('theme') || 'system';
  const applyTheme = (v) => {
    root.setAttribute('data-theme', v === 'system' ? (systemMedia.matches ? 'dark' : 'light') : v);
  };
  applyTheme(themeSel.value);
  
  themeSel.addEventListener('change', e => { 
    localStorage.setItem('theme', e.target.value); 
    applyTheme(e.target.value); 
  });
  
  systemMedia.addEventListener('change', () => {
    if (themeSel.value === 'system') applyTheme('system');
  });

  // 2. Prevent Background Page Scrolling when Mobile Drawer is Open
  if (masterToggle) {
    masterToggle.addEventListener('change', function() {
      document.body.style.overflow = this.checked ? 'hidden' : '';
    });
  }

  // 3. Perfect Native Dropdown Mutex Loop (Prevents Multi-Open Conflict)
  dropdowns.forEach(currentInput => {
    currentInput.addEventListener('click', function() {
      // If we are checking this input open, simulate a click on all other open menus
      if (this.checked) {
        dropdowns.forEach(otherInput => {
          if (otherInput !== currentInput && otherInput.checked) {
            // Triggering native click ensures the browser runs all CSS transition loops
            otherInput.click();
          }
        });
      }
    });
  });

  // 4. Global Reset Controls (Background Click-Away & Escape Key Handlers)
  const closeAllMenus = () => {
    // If the mobile hamburger drawer is open, click it to clear body scroll lock
    if (masterToggle && masterToggle.checked) masterToggle.click();
    
    // Explicitly click any open dropdown menus shut to sync animations smoothly
    dropdowns.forEach(checkbox => {
      if (checkbox.checked) checkbox.click();
    });
  };

  window.addEventListener('keydown', e => e.key === 'Escape' && closeAllMenus());
  
  document.addEventListener('click', (e) => {
    if (e.target.closest('.hp') || e.target.closest('.mt') || e.target.closest('.nw')) return;
    closeAllMenus();
  });
});
