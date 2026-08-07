document.addEventListener('DOMContentLoaded', () => {
    const resetBtn = document.getElementById('reset-btn');
    const tag = document.getElementById('current-dimension-tag');
    let reality = 'prime';

    document.querySelector('.timeline-container').addEventListener('click', (e) => {
        if (e.target.classList.contains('trigger-btn')) shift(e.target.dataset.target);
    });

    resetBtn.addEventListener('click', () => shift('prime'));

    function shift(target) {
        reality = target;
        document.body.className = reality !== 'prime' ? `state-${reality}` : '';
        resetBtn.classList.toggle('visible', reality !== 'prime');
        tag.textContent = `${reality.charAt(0).toUpperCase() + reality.slice(1)} Timeline`;

        document.querySelectorAll('.timeline-node').forEach(node => {
            const variants = Array.from(node.querySelectorAll('[data-node]'));
            let activeCard = variants.find(c => c.dataset.node === reality);
            
            if (!activeCard) {
                const parent = (reality === 'beta') ? 'prime' : 'alpha';
                activeCard = variants.find(c => c.dataset.node === parent);
            }

            variants.forEach(c => c.classList.toggle('hidden', c !== activeCard));
        });
    }
});




document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("nexus-random-gateway");
  if (!container) return;

  // Extract all pool questions and sort them into a completely random array
  const pool = Array.from(container.querySelectorAll(".pool-question"));
  const chosen = pool.sort(() => 0.5 - Math.random()).slice(0, 3);

  // Purge the 3 unused question nodes from the DOM instantly to clear tree memory overhead
  pool.forEach(node => { if (!chosen.includes(node)) node.remove(); });

  // Map the 3 chosen nodes to our highly optimized pure CSS active state tracking keys
  chosen.forEach((panel, index) => {
    const step = index + 1;
    panel.classList.add(`active-step-${step}`);
    panel.querySelector(".step-num").textContent = `0${step}`;

    // Link the correct path options directly to the active step's tracking checkbox id
    const correctBtn = panel.querySelector(".opt-correct-trigger");
    if (correctBtn) {
      correctBtn.setAttribute("role", "button");
      correctBtn.addEventListener("click", () => {
        document.getElementById(`q${step}-correct`).checked = true;
        // Trigger a synthetic change event to force rendering layers to repaint instantly
        document.getElementById(`q${step}-correct`).dispatchEvent(new Event("change", { bubbles: true }));
      });
    }
  });
});
