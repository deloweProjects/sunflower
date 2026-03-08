// ═══════════════════════════════════════════════════════
//   Project Sunflower — Global Configuration
// ═══════════════════════════════════════════════════════

// Explictly attach to window so it's accessible across different scopes/iframes
window.CONFIG = {
    // 1. UPLOAD YOUR BACKEND TO RENDER
    // 2. PASTE YOUR RENDER URL BELOW (e.g., 'https://sunflower-fuz9.onrender.com')
    // 3. IMPORTANT: NO TRAILING SLASH!
    API_BASE_URL: 'http://localhost:3000'
};

console.log('🌻 Config loaded:', window.CONFIG.API_BASE_URL);
