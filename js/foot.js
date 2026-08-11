document.addEventListener('click', (e) => {
  if (window.innerWidth < 1024 && !e.target.closest('#fa')) {
    document.querySelectorAll('.sf-state-toggle').forEach(radio => radio.checked = false);
  }
});
