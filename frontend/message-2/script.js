/* ═══════════════════════════════════════════════════════
   Project Sunflower — Message 2 Script (Redefined)
   Sequence: Happy Birthday → 21 → Black → Video → Done
   YouTube ID: Oby_Axy6eBA
═══════════════════════════════════════════════════════ */

const sleep = ms => new Promise(r => setTimeout(r, ms));

const STATE = {
    phases: {},
    player: null,
    apiReady: false
};

// ── YouTube API Setup ────────────────────
window.onYouTubeIframeAPIReady = () => {
    console.log("[YouTube] API Ready");
    STATE.player = new YT.Player('yt-player', {
        height: '100%',
        width: '100%',
        videoId: 'Oby_Axy6eBA',
        playerVars: {
            'autoplay': 1,
            'controls': 0,
            'rel': 0,
            'showinfo': 0,
            'modestbranding': 1,
            'loop': 0,
            'fs': 0,
            'cc_load_policy': 0,
            'iv_load_policy': 3,
            'autohide': 0,
            'mute': 1
        },
        events: {
            'onReady': () => {
                console.log("[YouTube] Player Ready");
                STATE.apiReady = true;
            },
            'onStateChange': (event) => {
                if (event.data == YT.PlayerState.ENDED) {
                    finishSequence();
                }
            }
        }
    });
};

async function startSequence() {
    STATE.phases = {
        hb: document.getElementById('m2-hb'),
        number: document.getElementById('m2-number'),
        vid: document.getElementById('m2-vid')
    };

    const number21 = document.getElementById('number-21');
    const particles = document.getElementById('number-particles');

    // ── Phase 1: Happy Birthday
    STATE.phases.hb.classList.add('active');
    await sleep(5000);
    STATE.phases.hb.classList.remove('active');
    await sleep(1500);

    // ── Phase 2: Number 21
    STATE.phases.number.classList.add('active');
    await sleep(300);
    number21.classList.add('reveal');
    if (particles) particles.classList.add('active');
    await sleep(4000);

    // ── Fade to black
    STATE.phases.number.classList.remove('active');
    await sleep(1500);

    // ── Phase 3: Video
    STATE.phases.vid.classList.add('active');

    // Wait for API if not ready
    let attempts = 0;
    while (!STATE.apiReady && attempts < 50) {
        await sleep(100);
        attempts++;
    }

    if (STATE.player && typeof STATE.player.playVideo === 'function') {
        STATE.player.unMute();
        STATE.player.playVideo();
    } else {
        console.warn("[YouTube] Player not ready, skipping to finish");
        finishSequence();
    }
}

async function finishSequence() {
    await sleep(1000);
    document.body.classList.add('fade-out');
    await sleep(2000);
    window.parent.postMessage({ type: 'm2-finished' }, '*');
}

// Start sequence on load
window.onload = startSequence;
