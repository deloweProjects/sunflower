/* ═══════════════════════════════════════════════════════
   Project Sunflower — intro/intro.js
   Precision cinematic engine with audio sync.
═══════════════════════════════════════════════════════ */

const STATE = {
    tapCount: 0,
    isIntroStarted: false
};

const EL = {
    tapContainer: document.getElementById('intro-tap-container'),
    cinematicContainer: document.getElementById('intro-cinematic-container'),
    sunflower: document.getElementById('sunflower-img'),
    zoomContainer: document.getElementById('sunflower-zoom-container'),
    text: document.getElementById('intro-text'),
    flash: document.getElementById('intro-flash'),
    audio: document.getElementById('intro-audio'),
    hint: document.getElementById('tap-hint'),
    labelPrefix: document.getElementById('label-prefix'),
    labelMain: document.getElementById('label-main')
};

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── SUNFLOWER TAP LOGIC ───────────────────
EL.sunflower.addEventListener('click', handleSunflowerTap);
EL.sunflower.addEventListener('touchend', e => {
    e.preventDefault();
    handleSunflowerTap();
});

function handleSunflowerTap() {
    if (STATE.isIntroStarted) return;
    STATE.tapCount++;

    // Tap feedback
    EL.sunflower.style.transform = 'scale(1.12)';
    setTimeout(() => {
        EL.sunflower.style.transform = '';
    }, 150);

    if (STATE.tapCount === 2) {
        EL.hint.style.opacity = '1';
        EL.hint.classList.add('visible');
    }

    if (STATE.tapCount >= 3) {
        startIntroSequence();
    }
}

// ── CINEMATIC ENGINE ──────────────────────
async function startIntroSequence() {
    STATE.isIntroStarted = true;
    document.body.classList.add('cinematic-active');

    // 1. ONE SECOND PAUSE
    await sleep(1000);

    // 2. SLOW FADE-IN OF "my" (2.5s)
    EL.labelPrefix.textContent = 'my';
    EL.labelPrefix.style.transition = 'opacity 2.5s ease';
    EL.labelPrefix.style.opacity = '1';
    await sleep(2500);

    // 3. THREE SECOND WAIT
    await sleep(3000);

    // 4. MUSIC STARTS + ROTATION (4s spin-only phase)
    EL.audio.src = 'assets/sound1.wav';
    EL.audio.play().catch(e => console.error("Audio playback failed:", e));

    EL.cinematicContainer.classList.add('active');

    // Fade label and hint
    EL.labelMain.style.opacity = '0';
    EL.labelPrefix.style.opacity = '0';
    EL.hint.style.opacity = '0';

    // Center the zoom container
    EL.zoomContainer.classList.add('cinematic');
    EL.zoomContainer.style.transition = 'none';
    EL.zoomContainer.style.transform = 'translate(-50%, -50%) scale(1)';
    setTimeout(() => {
        EL.zoomContainer.style.transition = 'transform 3s cubic-bezier(0.42, 0, 0.58, 1)';
    }, 0);

    // Start spinning
    EL.sunflower.style.animation = 'spinSlow 5s linear infinite';
    EL.text.style.opacity = '0';

    await sleep(4000);

    // 5. EXPANSION (3s)
    EL.zoomContainer.style.transition = 'transform 3s cubic-bezier(0.42, 0, 0.58, 1)';
    EL.zoomContainer.style.transform = 'translate(-50%, -50%) scale(100)';

    await sleep(3000);

    // 6. WHITE OUT (2s)
    document.body.classList.add('white-out');
    EL.sunflower.classList.add('white-out-symbol');
    EL.sunflower.style.opacity = '0';
    await sleep(2000);

    // 7. FADE TO BLACK, REVEAL "my SUNFLOWER" (2s)
    document.body.classList.remove('white-out');
    document.body.style.background = '#000';
    EL.text.style.transition = 'opacity 1.5s ease';
    EL.text.textContent = 'my SUNFLOWER';
    EL.text.style.opacity = '1';
    await sleep(2000);

    // 8. FADE OUT
    EL.text.style.opacity = '0';
    await sleep(2000);

    // 9. "Presenting"
    EL.text.textContent = 'Presenting';
    EL.text.style.opacity = '1';
    await sleep(2000);
    EL.text.style.opacity = '0';
    await sleep(1500);

    // 10. "PROJECT SUNFLOWER"
    EL.text.textContent = 'PROJECT SUNFLOWER';
    EL.text.style.opacity = '1';

    // 11. FADE OUT AT MUSIC END
    EL.audio.onended = async () => {
        EL.text.style.transition = 'opacity 3s ease';
        EL.text.style.opacity = '0';
        await sleep(3000);
        window.parent.postMessage({ type: 'intro-finished' }, '*');
    };

    // Fallback if audio doesn't fire onended (e.g. no audio file)
    setTimeout(() => {
        if (!STATE.introFinishedSent) {
            STATE.introFinishedSent = true;
            EL.text.style.transition = 'opacity 3s ease';
            EL.text.style.opacity = '0';
            setTimeout(() => {
                window.parent.postMessage({ type: 'intro-finished' }, '*');
            }, 3000);
        }
    }, 30000);
}