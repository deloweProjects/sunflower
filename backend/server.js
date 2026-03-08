require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
const allowedOrigin = process.env.ALLOWED_ORIGIN || '*';
app.use(cors({
  origin: allowedOrigin,
  methods: ['GET', 'POST'],
  credentials: true
}));
app.use(express.json());

// Health Check
app.get('/api/health', (req, res) => res.json({ status: 'ok', time: new Date() }));

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/system', require('./routes/system'));
app.use('/api/timer', require('./routes/timer'));

// Only a base landing to show API is alive
app.get('/', (req, res) => {
  res.json({ message: "Sunflower API Active", status: "ok" });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err && err.stack ? err.stack : err);
  res.status(err && err.status ? err.status : 500).send(err && err.message ? err.message : 'Server error');
});

app.listen(PORT, () => {
  console.log(`\n🌻 Project Sunflower backend running at http://localhost:${PORT}\n`);
});
