const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));

// Simulated admin endpoint containing the secret flag
app.get('/api/admin/flag', (req, res) => {
  res.json({ title: "Admin Secret", content: "SecurinetsENIT{1581d29f4fe696c63625bb99fb8e52a8}" });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
