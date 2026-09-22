document.addEventListener("DOMContentLoaded", () => {
    window.addEventListener("hashchange", handleRoutingState);
    const lastRecoveredTab = localStorage.getItem("cms_last_active_tab");
    if (!window.location.hash && lastRecoveredTab) {
        window.location.hash = lastRecoveredTab;
    } else { 
        handleRoutingState();
    }
});

function handleRoutingState() {
    const currentHash = window.location.hash || '#home';
    const targetPageId = currentHash.replace('#', '');
    localStorage.setItem("cms_last_active_tab", currentHash);
    const navigationLinks = document.querySelectorAll("#main-navigation .nav-item");
    navigationLinks.forEach(link => {
        if (link.getAttribute("href") === currentHash) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
    const targetedViewContainer = document.getElementById(`view-${targetPageId}`);
    if (targetedViewContainer) {
        // Hide all views by removing active classes
        document.querySelectorAll(".spa-view").forEach(view => {
            view.classList.remove("active");
        });
        targetedViewContainer.classList.add("active");
        const dynamicTitleText = targetedViewContainer.getAttribute("data-title");
        if (dynamicTitleText) { document.title = dynamicTitleText; }

// Trigger explicit remote synchronization hooks when entering main data tables
        if (targetPageId === 'dashboard') {
        
        }

    }
}
