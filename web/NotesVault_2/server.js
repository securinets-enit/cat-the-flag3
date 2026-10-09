const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Serve static assets
app.use(express.static(path.join(__dirname, 'public')));

// Simulated Backend WAF Middleware
app.use('/api', (req, res, next) => {
  const rawUrl = req.originalUrl;

  // Rule 1: Block dot-dot sequences in raw or decoded form
  if (rawUrl.includes('..') || decodeURIComponent(rawUrl).includes('..')) {
    return res.status(403).json({ error: "WAF: Path Traversal Detected (..)" });
  }

  // Rule 2: Block encoded slashes (%2f, %2F, %5c, %5C)
  if (/%2f|%2F|%5c|%5C/.test(rawUrl)) {
    return res.status(403).json({ error: "WAF: Encoded Slashes Prohibited" });
  }

  // Rule 3: Block double encoding attempts
  if (/%25/.test(rawUrl)) {
    return res.status(403).json({ error: "WAF: Double Encoding Detected" });
  }

  next();
});

// Standard API Endpoint
app.get('/api/v1/notes/:noteId', (req, res) => {
  const noteId = req.params.noteId;
  
  if (noteId === 'welcome') {
    return res.json({
      title: "Welcome Note",
      content: "Welcome to Vault v2! Traversal is now strictly monitored by our WAF."
    });
  }

  res.status(404).json({ error: "Note not found" });
});

// Flag Endpoint (Protected)
app.get('/api/v1/admin/flag', (req, res) => {
  res.json({
    title: "Flag Captured!",
    content: "CTF{c2p7_w4f_byp4ss_v14_url_p4rs3r_3xp1017}"
  });
});

app.listen(PORT, () => {
  console.log(`Hard CSPT Challenge listening on port ${PORT}`);
});
