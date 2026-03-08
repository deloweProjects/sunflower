const express = require('express');
const router = express.Router();

// Credentials
const VALID_CREDENTIALS = [
    { name: 'gemma', password: 'iwantmore', type: 'wrong_name' },
    { name: 'EllyG', password: 'iwantmore', type: 'correct' }
];

// POST /api/auth
router.post('/', (req, res) => {
    const { name, password } = req.body;
    if (!name || !password) return res.status(400).json({ error: 'Missing credentials' });

    const inputName = name.trim().toLowerCase();
    const inputPass = password.trim();

    // First default: gemma / iwantmore
    if (inputName === 'gemma' && inputPass === 'iwantmore') {
        return res.json({ status: 'wrong_name', message: "wrong name, correct name is 'EllyG'" });
    }
    // Correct: EllyG / iwantmore
    if (inputName === 'ellyg' && inputPass === 'iwantmore') {
        return res.json({ status: 'correct', message: 'Access granted' });
    }
    // Admin: alpha / iammore
    if (inputName === 'alpha' && inputPass === 'iammore') {
        return res.json({ status: 'admin', message: 'ADMIN ACCESS GRANTED' });
    }
    // Right password wrong name
    if (inputPass === 'iwantmore' && inputName !== 'ellyg') {
        return res.json({ status: 'wrong_name_only', message: "your password was right, just use name = 'EllyG'" });
    }
    // Completely wrong
    return res.json({ status: 'denied', message: 'you are not allowed' });
});

module.exports = router;
