const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

const sessionsDir = path.join(__dirname, '..', 'sessions');

function loadSession(id) {
    const file = path.join(sessionsDir, `${id}.json`);
    if (fs.existsSync(file)) return JSON.parse(fs.readFileSync(file, 'utf8'));
    return null;
}

function saveSession(session) {
    const file = path.join(sessionsDir, `${session.session_id}.json`);
    fs.writeFileSync(file, JSON.stringify(session, null, 2));
}

// POST /api/session/start
router.post('/start', (req, res) => {
    const { player_id } = req.body;

    // Check if existing session for this player
    const files = fs.readdirSync(sessionsDir);
    let existing = null;
    for (const f of files) {
        const s = JSON.parse(fs.readFileSync(path.join(sessionsDir, f), 'utf8'));
        if (s.player_id === player_id) { existing = s; break; }
    }

    if (existing) {
        return res.json({
            session_id: existing.session_id,
            bond_state: existing.bond_state,
            emotional_state: existing.emotional_state,
            checkpoint: existing.checkpoint,
            progress_percent: existing.progress_percent,
            resuming: true
        });
    }

    const session = {
        session_id: uuidv4(),
        player_id: player_id || 'EllyG',
        is_admin: player_id === 'alpha',
        bond_state: { trust: 50, aggression: 0, resentment: 10, dependency: 0 },
        emotional_state: 'observing',
        checkpoint: 0,
        progress_percent: 0,
        entity_states: { darks: [], gemma_active: true, ziah_active: false },
        dialogue_history: [],
        start_time: new Date().toISOString(),
        phase: 'maze', // 'maze' | 'radial' | 'complete'
        maze_won: false,
        radial_won: false
    };

    saveSession(session);
    res.json({
        session_id: session.session_id,
        bond_state: session.bond_state,
        emotional_state: session.emotional_state,
        ai_initial_state: 'observing',
        resuming: false
    });
});

// GET /api/session/:id
router.get('/:id', (req, res) => {
    const session = loadSession(req.params.id);
    if (!session) return res.status(404).json({ error: 'Session not found' });
    res.json(session);
});

// PATCH /api/session/:id — update arbitrary fields
router.patch('/:id', (req, res) => {
    const session = loadSession(req.params.id);
    if (!session) return res.status(404).json({ error: 'Session not found' });
    const updates = req.body;
    Object.assign(session, updates);
    saveSession(session);
    res.json({ ok: true, session });
});

module.exports = router;
module.exports.loadSession = loadSession;
module.exports.saveSession = saveSession;
