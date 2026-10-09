# Hints · 10 mirage

**Hint 1 (free):** The dashboard tells you straight out that your role can't run
maintenance jobs — those are admin-only, and the flag only comes from running
one. So you need two things: become admin, *and* make the maintenance job do
something it shouldn't. Neither bug alone is enough.

**Hint 2 (becoming admin):** How are you authenticated? Look at your `token`
cookie — it's a JWT (`header.payload.signature`), `alg: HS256`. HS256 is
symmetric: the secret that *signs* is the secret that *verifies*. If the secret
is weak, you can recover it offline and sign your own tokens.
```
hashcat -m 16500 token.jwt rockyou.txt      # or jwt_tool / john
```
The secret is a single lowercase dictionary word (an internal project codename) —
present in common wordlists, not something you'd guess blind. Once you have it,
forge a token with `"role":"admin"`.

**Hint 3 (don't bother polluting your role):** You may notice a hidden endpoint
that merges JSON into your profile (see Hint 4) — but trying to set `role`,
`isAdmin`, etc. to reach admin is a dead end by design. Authorization reads the
role from your *signed token* as an own property, and every token already carries
an explicit `role`, so a polluted prototype never wins. Cracking the JWT is the
only road to admin. (The "report a concern" box is also a decoy — it goes
nowhere.)

**Hint 4 (the second bug):** On the dashboard, watch the Network tab: the page
silently does `GET /users/<your-id>`. That endpoint also accepts **POST**, and it
*deep-merges* your JSON body into your profile with no `__proto__` guard — classic
server-side **prototype pollution**. It's IDOR-locked to your own id, so it's only
good for polluting `Object.prototype`, nothing else.

**Hint 5 (from pollution to RCE):** The admin maintenance job runs a Node worker
with `child_process.fork()` and returns the worker's **log** in the response.
`fork` honors an `execArgv` array (extra `node` flags) on its options. The app
builds those options by *copying* a config object, which pulls in inherited
properties — so if you pollute `Object.prototype.execArgv`, it lands on the real
options and the worker launches with your flags. Use `--eval` to print the flag to
the job's stdout — **no file drop, no second request:**
```json
POST /users/<your-id>   (as the normal user)
{"__proto__":{"execArgv":["--eval=console.log(require('fs').readFileSync('/flag.txt','utf8'))"]}}
```
Then trigger the job as admin (`POST /admin/maintenance` with your forged token)
and read the flag straight out of the returned `log`.

**Hint 6 (why the "obvious" version fails):** If you polluted `execArgv` and the
job still ran clean, note: on modern Node a bare options object whose *prototype*
is polluted does **not** pass the flag through — `child_process` reads own
properties only. It works here because the app's config-copy turns the inherited
`execArgv` into an own property first. Pollute, then trigger; the order matters
and the pollution is process-wide.
