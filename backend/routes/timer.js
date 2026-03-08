const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    // Target date: March 11, 2026 00:00:00 UTC
    const targetDate = new Date("2026-03-11T00:00:00Z");
    const now = new Date();

    const remainingMs = Math.max(targetDate - now, 0);

    const days = Math.floor(remainingMs / (1000 * 60 * 60 * 24));
    const hours = Math.floor((remainingMs / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((remainingMs / (1000 * 60)) % 60);
    const seconds = Math.floor((remainingMs / 1000) % 60);

    res.json({
        serverTime: now.getTime(),
        targetTime: targetDate.getTime(),
        remainingMs,
        breakdown: {
            days,
            hours,
            minutes,
            seconds
        }
    });
});

module.exports = router;
