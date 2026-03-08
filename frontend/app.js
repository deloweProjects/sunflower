/* ═══════════════════════════════════════════════════════
   Project Sunflower — app.js (Luxury Orchestrator)
═══════════════════════════════════════════════════════ */

const API_BASE_URL = window.CONFIG ? window.CONFIG.API_BASE_URL : '';

if (!API_BASE_URL) {
    console.warn("⚠️ API_BASE_URL is not set. Local testing defaults will be used.");
} else if (window.location.hostname !== 'localhost' && API_BASE_URL.includes('localhost')) {
    console.error("❌ CRITICAL: Your live site is trying to connect to a local backend. Update config.js with your Render URL!");
} else {
    console.log(`✅ API Connection: ${API_BASE_URL}`);
}
// ── Configuration ──────────────────────────
// No hardcoded target date here — we fetch from the server for precision and security.

// ── State ─────────────────────────────────
const STATE = {
    phase: 'splash',
    tapCount: 0,
    touchStartY: 0,
    isLoggedIn: false,
    isAdmin: false,
    timerExpired: false,
    timerInterval: null,
    syncInterval: null,
    remainingMs: 0,
    syncTimeStamp: 0 // Using performance.now() for monotonic stability
};

// ── DOM refs ──────────────────────────────
const EL = {};
const ids = [
    'phase-splash', 'phase-login', 'phase-intro', 'phase-timer',
    'phase-gift', 'phase-shell', 'main-frame', 'intro-frame',
    'splash-text', 'splash-hint', 'splash-video',
    'login-name', 'login-pass', 'login-btn', 'login-message',
    'timer-display', 'transition-overlay', 'admin-skip-menu', 'gift-btn'
];
ids.forEach(id => { EL[id] = document.getElementById(id); });

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── API helpers ───────────────────────────
async function apiPost(path, body) {
    try {
        console.log(`[API] POST ${path}`, body);
        const r = await fetch(API_BASE_URL + path, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const data = await r.json();
        console.log(`[API] RESPONSE`, data);
        return data;
    } catch (e) {
        console.error(`[API] ERROR`, e);
        return {};
    }
}

// ══════════════════════════════════════════════
//  PHASE MANAGEMENT
// ══════════════════════════════════════════════

function showPhase(name) {
    STATE.phase = name;
    document.querySelectorAll('.phase').forEach(p => {
        p.classList.remove('active');
    });

    switch (name) {
        case 'splash':
            EL['phase-splash']?.classList.add('active');
            break;
        case 'login':
            EL['phase-login']?.classList.add('slide-up', 'active');
            break;
        case 'intro':
            EL['phase-splash']?.classList.remove('active');
            EL['phase-login']?.classList.remove('slide-up');
            EL['phase-intro']?.classList.add('active');
            EL['intro-frame'].src = 'intro/index.html';
            break;
        case 'timer':
            EL['phase-intro']?.classList.remove('active');
            EL['phase-timer']?.classList.add('active');
            startCountdown();
            break;
        case 'gift':
            EL['phase-timer']?.classList.remove('active');
            EL['phase-gift']?.classList.add('active');
            break;
        case 'message1':
            EL['phase-gift']?.classList.remove('active');
            EL['phase-shell']?.classList.add('active');
            EL['main-frame'].src = 'message-1/index.html';
            break;
        case 'message2':
            console.log(`[Phase] Switching to ${name}`);
            EL['phase-shell']?.classList.add('active');
            EL['main-frame'].src = 'message-2/index.html';
            break;
        case 'final':
            console.log(`[Phase] Switching to ${name}`);
            EL['phase-shell']?.classList.add('active');
            EL['main-frame'].src = 'finalweb/index.html';
            break;
    }
}

async function transitionTo(phase) {
    const overlay = EL['transition-overlay'];
    overlay.classList.add('active');
    await sleep(1500); // Slower luxury transition
    showPhase(phase);
    await sleep(800);
    overlay.classList.remove('active');
}

// ══════════════════════════════════════════════
//  SPLASH & LOGIN FLOW
// ══════════════════════════════════════════════

// ── Video Loading ────────────────────────
if (EL['splash-video']) {
    const handleVideoReady = () => {
        EL['splash-video'].classList.add('loaded');
        EL['splash-video'].play().catch(e => console.warn("Splash video autoplay failed", e));
    };

    // Use both events to ensure it shows up as soon as any data is ready
    EL['splash-video'].addEventListener('canplay', handleVideoReady);
    EL['splash-video'].addEventListener('canplaythrough', handleVideoReady);
}

EL['phase-splash']?.addEventListener('click', () => {
    STATE.tapCount++;
    if (STATE.tapCount >= 1) { // Reduced for better UX since we have swipe hint now
        EL['splash-hint'].classList.add('visible');
        enableSlideGesture();
    }
});

function enableSlideGesture() {
    const splash = EL['phase-splash'];
    if (splash.dataset.gestureEnabled) return;
    splash.dataset.gestureEnabled = 'true';

    splash.addEventListener('touchstart', (e) => {
        STATE.touchStartY = e.touches[0].clientY;
    }, { passive: true });

    splash.addEventListener('touchend', (e) => {
        const diff = STATE.touchStartY - e.changedTouches[0].clientY;
        if (diff > 60) revealLogin();
    });

    // Desktop swipe simulation (drag up)
    let isDragging = false;
    let dragStart = 0;

    splash.addEventListener('mousedown', (e) => {
        isDragging = true;
        dragStart = e.clientY;
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const dragDiff = dragStart - e.clientY;
        if (dragDiff > 100) {
            isDragging = false;
            revealLogin();
        }
    });

    window.addEventListener('mouseup', () => {
        isDragging = false;
    });

    // Click fallback
    splash.addEventListener('click', () => {
        if (STATE.tapCount >= 5) revealLogin();
    });
}

async function revealLogin() {
    if (STATE.phase === 'login') return;
    EL['phase-splash'].style.opacity = '0';
    showPhase('login');
    await sleep(1500);
    EL['phase-splash'].classList.remove('active');
}

EL['login-btn']?.addEventListener('click', doLogin);
EL['login-pass']?.addEventListener('keydown', e => { if (e.key === 'Enter') doLogin(); });

async function doLogin() {
    const name = EL['login-name'].value.trim();
    const pass = EL['login-pass'].value.trim();
    if (!name || !pass) return;

    console.log(`[Login] Attempting for: ${name}`);
    EL['login-btn'].textContent = 'VERIFYING...';
    const res = await apiPost('/api/auth', { name, password: pass });

    if (res.status === 'correct' || res.status === 'admin') {
        STATE.isLoggedIn = true;
        console.log(`[Login] SUCCESS: ${res.status}`);
        if (res.status === 'admin') {
            STATE.isAdmin = true;
            EL['admin-skip-menu'].classList.remove('hidden');
            console.log(`[Admin] Bypassing restrictions.`);
        }
        await transitionTo('intro');
    } else {
        console.warn(`[Login] FAILED: ${res.message || 'Unknown'}`);
        EL['login-message'].textContent = '( INVALID IDENTITY )';
        EL['login-btn'].textContent = 'VERIFY';
    }
}

// ══════════════════════════════════════════════
//  ADMIN: SKIP PHASES
// ══════════════════════════════════════════════

window.adminSkip = (phase) => {
    if (!STATE.isAdmin) return;
    if (STATE.timerInterval) clearInterval(STATE.timerInterval);
    transitionTo(phase);
};

// ══════════════════════════════════════════════
//  TIMER & GIFT
// ══════════════════════════════════════════════

async function startCountdown() {
    await syncTimer();

    // UI update interval (1s)
    if (STATE.timerInterval) clearInterval(STATE.timerInterval);
    STATE.timerInterval = setInterval(updateTimer, 1000);

    // Periodic re-sync (30s) to handle network latency or extreme drift
    if (STATE.syncInterval) clearInterval(STATE.syncInterval);
    STATE.syncInterval = setInterval(syncTimer, 30000);
}

async function syncTimer() {
    console.log('[Timer] Synchronizing with server...');
    try {
        const start = performance.now();
        const res = await fetch(API_BASE_URL + '/api/timer');
        const data = await res.json();
        const end = performance.now();

        // Precision adjustment: subtract half the round-trip time
        const rtt = end - start;
        STATE.remainingMs = data.remainingMs - (rtt / 2);
        STATE.syncTimeStamp = performance.now();

        console.log(`[Timer] Synced. Remaining: ${Math.round(STATE.remainingMs / 1000)}s (RTT: ${Math.round(rtt)}ms)`);
        updateTimer();
    } catch (e) {
        console.error('[Timer] Sync failed:', e);
    }
}

function updateTimer() {
    // The trick: Calculate current remaining time relative to the last sync 
    // using performance.now(), which is NOT affected by system clock changes.
    const elapsedSinceSync = performance.now() - STATE.syncTimeStamp;
    const currentRemaining = Math.max(0, STATE.remainingMs - elapsedSinceSync);

    if (currentRemaining <= 0) {
        clearInterval(STATE.timerInterval);
        clearInterval(STATE.syncInterval);
        EL['timer-display'].textContent = '00 : 00 : 00 : 00';
        STATE.timerExpired = true;
        setTimeout(() => transitionTo('gift'), 2000);
        return;
    }

    const d = Math.floor(currentRemaining / 86400000);
    const h = Math.floor((currentRemaining % 86400000) / 3600000);
    const m = Math.floor((currentRemaining % 3600000) / 60000);
    const s = Math.floor((currentRemaining % 60000) / 1000);

    const pad = n => String(n).padStart(2, '0');
    EL['timer-display'].textContent = `${pad(d)} : ${pad(h)} : ${pad(m)} : ${pad(s)}`;
}

EL['gift-btn']?.addEventListener('click', async () => {
    console.log('[Gift] Button clicked');
    EL['gift-btn'].style.transform = 'scale(1.5)';
    EL['gift-btn'].style.opacity = '0';
    await sleep(1000);
    await transitionTo('message1');
});

// ══════════════════════════════════════════════
//  IFRAME BRIDGE
// ══════════════════════════════════════════════

window.addEventListener('message', async (e) => {
    const msg = e.data;
    if (msg === 'intro-finished' || msg.type === 'intro-finished') transitionTo('timer');
    if (msg === 'm1-finished' || msg.type === 'm1-finished') {
        console.log('[Message 1] Finished. Waiting before Phase 2...');
        await sleep(5000); // 5 second luxury buffer as requested
        showPhase('message2');
    }
    if (msg === 'm2-finished' || msg.type === 'm2-finished') transitionTo('final');

    if (msg === 'replay-intro') showPhase('intro');
    if (msg === 'replay-msg1') showPhase('message1');
    if (msg === 'replay-msg2') showPhase('message2');
});
