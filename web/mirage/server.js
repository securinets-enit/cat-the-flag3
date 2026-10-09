'use strict';

/*
 * Mirage — Industrial Systems internal portal.
 *
 * Intended chain (two independent bugs, both required):
 *   1. Auth issues an HS256 JWT signed with a weak, crackable secret. Crack it
 *      offline, forge a token with role:"admin" -> reach the admin-only
 *      "maintenance job" endpoint.
 *   2. The hidden /users/:id endpoint (the dashboard GETs it silently) accepts
 *      POST and deep-merges the JSON body into the caller's own profile WITHOUT
 *      guarding __proto__ -> server-side prototype pollution. The admin job
 *      fork()s a Node worker; its options bag is assembled by copying a config
 *      object (for..in), which materialises the polluted Object.prototype.execArgv
 *      as an OWN property -> the forked node runs attacker flags -> RCE.
 *
 * Authorisation is deliberately PP-proof: admin is decided only from the
 * signature-verified JWT payload, read via Object.hasOwn(), and every token
 * (including normal users') carries an explicit own `role` claim. Prototype
 * pollution therefore cannot forge admin — only cracking the secret can.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const express = require('express');
const cookieParser = require('cookie-parser');
const jwt = require('jsonwebtoken');

const views = require('./views');
const { runMaintenanceJob } = require('./jobs/runner');

const PORT = parseInt(process.env.PORT || '8010', 10);
const INTERNAL_BASE = `http://127.0.0.1:${PORT}`;

// Weak HMAC signing key. Themed internal project codename — crackable from a
// common wordlist (rockyou), but not blind-guessable and not the app name.
const JWT_SECRET = process.env.JWT_SECRET || 'fenrir';

// In-memory user store. Each user has a numeric id and a free-form `profile`
// object that the /users/:id merge writes into.
const users = new Map(); // username -> { id, username, password, profile }
let nextId = 1000;

function makeUser(username, password) {
  const id = nextId++;
  const user = {
    id,
    username,
    password,
    profile: { displayName: username, title: 'Operator', theme: 'dark' },
  };
  users.set(username, user);
  return user;
}

// Seed an admin account nobody can log into (random password); it exists only
// so "admin" is a real role, never a login shortcut.
makeUser('admin', crypto.randomBytes(24).toString('hex')).profile.title =
  'Site Administrator';

function sign(user) {
  // IMPORTANT: always issue an explicit own `role` claim, even for normal users,
  // so authz never falls through to a polluted Object.prototype.role.
  const role = user.username === 'admin' ? 'admin' : 'user';
  return jwt.sign(
    { sub: user.username, uid: user.id, role },
    JWT_SECRET,
    { algorithm: 'HS256', expiresIn: '2h' }
  );
}

const app = express();
app.disable('x-powered-by');
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));

// ---- JWT middleware: decode token from cookie or Authorization header -------
app.use((req, _res, next) => {
  let token = req.cookies && req.cookies.token;
  const auth = req.headers.authorization || '';
  if (!token && auth.startsWith('Bearer ')) token = auth.slice(7);
  req.jwt = null;
  if (token) {
    try {
      req.jwt = jwt.verify(token, JWT_SECRET, { algorithms: ['HS256'] });
    } catch (_) {
      req.jwt = null;
    }
  }
  next();
});

function requireAuth(req, res, next) {
  if (!req.jwt) return res.status(401).json({ error: 'authentication required' });
  next();
}

// Admin decided ONLY from the signed payload, read as an OWN property. A user who
// pollutes Object.prototype.role = "admin" still fails here: hasOwn is false on
// the prototype, so forging admin requires signing with the cracked secret.
function requireAdmin(req, res, next) {
  const p = req.jwt;
  if (p && Object.hasOwn(p, 'role') && p.role === 'admin') return next();
  return res.status(403).json({ error: 'admin role required' });
}

// ---- Vulnerable deep-merge (no __proto__ guard) -----------------------------
// Used to apply profile updates. Recurses into nested objects, so a body of
// {"__proto__":{"execArgv":[...]}} walks into Object.prototype and pollutes it.
function deepMerge(target, source) {
  for (const key in source) {
    const val = source[key];
    if (val && typeof val === 'object' && !Array.isArray(val)) {
      if (!target[key] || typeof target[key] !== 'object') target[key] = {};
      deepMerge(target[key], val);
    } else {
      target[key] = val;
    }
  }
  return target;
}

// ---- Pages ------------------------------------------------------------------
app.get('/', (req, res) => {
  if (!req.jwt) return res.redirect('/login');
  res.send(views.dashboardPage({ jwt: req.jwt }));
});

app.get('/login', (req, res) => {
  if (req.jwt) return res.redirect('/');
  res.send(views.loginPage({ mode: 'login', error: null }));
});

app.get('/signup', (req, res) => {
  if (req.jwt) return res.redirect('/');
  res.send(views.loginPage({ mode: 'signup', error: null }));
});

// ---- Auth API ---------------------------------------------------------------
function setToken(res, user) {
  // NOT httpOnly: operators inspect their own token in the portal. (It is the
  // player's own token to attack — the whole point of the auth bug.)
  res.cookie('token', sign(user), { sameSite: 'lax', path: '/' });
}

app.post('/api/signup', (req, res) => {
  const username = String((req.body && req.body.username) || '').trim();
  const password = String((req.body && req.body.password) || '');
  if (!username || !password)
    return res.status(400).json({ error: 'username and password required' });
  if (!/^[A-Za-z0-9_.-]{1,32}$/.test(username))
    return res.status(400).json({ error: 'invalid username' });
  if (users.has(username))
    return res.status(409).json({ error: 'username already exists' });
  const user = makeUser(username, password);
  setToken(res, user);
  res.json({ ok: true, token: sign(user), id: user.id, role: 'user' });
});

app.post('/api/login', (req, res) => {
  const username = String((req.body && req.body.username) || '').trim();
  const password = String((req.body && req.body.password) || '');
  const user = users.get(username);
  if (!user || user.password !== password)
    return res.status(401).json({ error: 'invalid credentials' });
  setToken(res, user);
  const role = username === 'admin' ? 'admin' : 'user';
  res.json({ ok: true, token: sign(user), id: user.id, role });
});

app.post('/api/logout', (req, res) => {
  res.clearCookie('token', { path: '/' });
  res.json({ ok: true });
});

// ---- Hidden profile endpoint (dashboard GETs it; it also accepts POST) ------
function findById(id) {
  for (const u of users.values()) if (String(u.id) === String(id)) return u;
  return null;
}

app.get('/users/:id', requireAuth, (req, res) => {
  // IDOR-protected: you may only read your OWN record.
  if (String(req.params.id) !== String(req.jwt.uid))
    return res.status(403).json({ error: 'forbidden' });
  const u = findById(req.params.id);
  if (!u) return res.status(404).json({ error: 'not found' });
  res.json({ id: u.id, username: u.username, role: req.jwt.role, profile: u.profile });
});

app.post('/users/:id', requireAuth, (req, res) => {
  // IDOR-protected to your own record — so this is never a path to another
  // user's object or to privilege; it only merges into your own profile.
  if (String(req.params.id) !== String(req.jwt.uid))
    return res.status(403).json({ error: 'forbidden' });
  const u = findById(req.params.id);
  if (!u) return res.status(404).json({ error: 'not found' });
  const body = req.body && typeof req.body === 'object' ? req.body : {};
  deepMerge(u.profile, body); // <-- unsafe merge: prototype pollution sink
  res.json({ ok: true, profile: u.profile });
});

// ---- Admin maintenance job (the fork sink) ----------------------------------
app.get('/admin/maintenance', requireAuth, requireAdmin, (req, res) => {
  res.json({
    ok: true,
    hint: 'POST here to run the search-index rebuild worker.',
  });
});

app.post('/admin/maintenance', requireAuth, requireAdmin, async (req, res) => {
  try {
    const result = await runMaintenanceJob();
    // Return the worker's log so operators can see the job output.
    res.json({ ok: true, job: 'index-rebuild', code: result.code, log: result.log });
  } catch (e) {
    res.status(500).json({ error: 'job failed to start', detail: String(e && e.message) });
  }
});

app.listen(PORT, () => {
  console.log(`[mirage] portal on ${INTERNAL_BASE}  (PORT=${PORT})`);
});
