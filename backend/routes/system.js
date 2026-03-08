const express = require('express');
const router = express.Router();

// March 9, 2026 — radial maze unlock date
const RADIAL_DATE = new Date('2026-03-09T00:00:00+02:00');
// March 11, 2026 — gift/birthday reveal date
const FINAL_DATE = new Date('2026-03-11T00:00:00+02:00');

// GET /api/system/date-check
router.get('/date-check', (req, res) => {
    const { session_id } = req.query;

    // Server time is the source of truth
    const now = new Date();

    let isAdmin = false;
    if (session_id) {
        try {
            const { loadSession } = require('./session');
            const session = loadSession(session_id);
            if (session && session.is_admin) isAdmin = true;
        } catch (e) { }
    }

    res.json({
        server_time: now.toISOString(),
        server_ms: now.getTime(),

        // Conditions
        radial_unlocked: isAdmin || now >= RADIAL_DATE,
        final_unlocked: isAdmin || now >= FINAL_DATE,

        // Precise remaining MS
        ms_until_radial: Math.max(0, RADIAL_DATE - now),
        ms_until_final: Math.max(0, FINAL_DATE - now),

        isAdmin
    });
});

module.exports = router;
