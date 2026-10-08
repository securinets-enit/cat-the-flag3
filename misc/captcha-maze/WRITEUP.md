# Writeup: Captcha: Rats in a Maze

**Author:** MrXFuji  
**Category:** Misc / Automation / Algorithmic  
**Difficulty:** ⭐⭐⭐ Hard  
**Target Flag:** `Securinets{d3sp1t3_all_OuR_rag3_w3_ar3_all_ju5t_rat5_1n_a_maz3}`

---

## 1. Initial Reconnaissance

Connecting to the challenge endpoint via OpenSSL:
```bash
openssl s_client -connect challenge.securinets.tn:5000 -quiet
```

The service displays:
```text
============================================================
    SecurinetsENIT CTF - Captcha: Rats in a Maze v1.0       
============================================================
Welcome, user.
A simple captcha to prove you're not a robot.
Clear 100 consecutive 11x11 maze rounds within 5.0s each.

proof of work: curl -sSfL https://pwn.red/pow | sh -s s.AAAAZA==.5vhQKR3MpuZBb+qE3Gp3IQ==
solution:
```

We are immediately faced with:
1. A **Proof of Work** banner using `redpwn/pow`.
2. A sequence of **100 dynamically generated 11×11 mazes**.
3. A **5.0-second deadline per maze**.

Humans cannot parse 11×11 weighted mazes, calculate shortest paths, and type ~30-step move sequences within 5 seconds 100 times in a row. A robotic automated client is mandatory.

---

## 2. Overcoming the Traps

### Trap 1: The Redpwn Proof-of-Work
The banner issues a standard challenge:
`curl -sSfL https://pwn.red/pow | sh -s <challenge>`

While you can shell out to the bash command via `subprocess.run()`, under the hood `redpwn/pow` uses a Verifiable Delay Function (VDF) over a Mersenne prime field:
$$\text{mod} = 2^{1279} - 1, \quad \text{exp} = 2^{1277}$$
Each step computes:
$$x \leftarrow (x^{\text{exp}} \bmod \text{mod}) \oplus 1$$
We can implement this directly in Python using native arbitrary-precision integers:
```python
def solve_redpwn_pow(chal_str):
    parts = chal_str.strip().split('.')
    d = int.from_bytes(base64.b64decode(parts[1]), 'big')
    x = int.from_bytes(base64.b64decode(parts[2]), 'big')
    for _ in range(d):
        x = pow(x, 1 << 1277, (1 << 1279) - 1) ^ 1
    return f"s.{base64.b64encode(x.to_bytes(160, 'big')).decode()}"
```
This computes in $\approx 0.3$ seconds without external shell overhead.

---

### Trap 2: Blind ANSI Stripping Destroys Entrances and Exits
The maze is rendered in color:
- The **Entrance** is an opening in the outer border colored with **Green** (`\x1b[92m`).
- The **Exit** is an opening in the outer border colored with **Red** (`\x1b[91m`).
- Internal walls are colored cyan (`\x1b[36m`).

If a solver naively strips all ANSI escape codes using `re.sub(r'\x1b\[[0-9;]*m', '', line)`, the green and red colors disappear! The maze borders become identical `═` and `║` characters, making it impossible to determine where to start and where to finish.

**Solution:** Parse characters *together* with their active ANSI styling:
```python
def tokenize_ansi_line(line):
    tokens = []
    active_color = None
    i = 0
    while i < len(line):
        if line[i] == '\x1b':
            m = ANSI_REGEX.match(line, i)
            if m:
                if '92m' in m.group(0): active_color = 'green'
                elif '91m' in m.group(0): active_color = 'red'
                elif '0m' in m.group(0): active_color = None
                i = m.end()
                continue
        tokens.append((line[i], active_color))
        i += 1
    return tokens
```

---

### Trap 3: East Asian Double-Width Unicode Alignment (UAX #11)
In terminal fonts, each maze cell occupies **2 terminal display columns**:
- ASCII walls: `# ` (1 character + 1 space = 2 columns).
- Middle dots: `· ` (1 character + 1 space = 2 columns).
- Narrow pieces (Chess `♙`, Dice `⚀`): 1 character + 1 space = 2 columns.
- **Wide pieces (Dominoes `🁣`, Mahjong `🀐`, Cards `🂡`)**: 1 character alone takes **2 visual columns**!

Because of this, the raw string sent over the socket does **not** have a space following wide characters:
- Cell with wall: `len("# ") == 2`
- Cell with Mahjong: `len("🀐") == 1`

If you attempt string indexing like `cell = row[col*2 : col*2+2]`, every single cell to the right of any wide character will be offset by 1 column, completely corrupting the board.

**Solution:** Advance the parsing index based on character width:
```python
if is_wide(ch):
    grid[(r, c)] = ch
    idx += 1  # Wide character takes the full 2 columns!
else:
    grid[(r, c)] = ch
    idx += 2  # Narrow character is followed by a space padding
```

---

### Trap 4: Mandatory Border Moves
The entrance and exit are located on the outer bounding box:
- Green segment on **Top** border $\implies$ Mandatory first move is **`D`** (Down into cell `(0, c)`).
- Green segment on **Left** border $\implies$ Mandatory first move is **`R`** (Right into cell `(r, 0)`).
- Green segment on **Bottom** border $\implies$ Mandatory first move is **`U`** (Up into cell `(10, c)`).
- Green segment on **Right** border $\implies$ Mandatory first move is **`L`** (Left into cell `(r, 10)`).

The exit dictates the mandatory final move into the red border segment similarly.

---

## 3. Piece Cost Model

Moving onto any tile incurs a base cost of `1` plus the piece's toll:
$$\text{Cost}(v) = 1 + \text{weight}(v)$$

| Category | Range / Formula | Value |
|---|---|---|
| **Chess** | `♙` (1), `♘`/`♗` (3), `♖` (5), `♕` (9), `♔` (100) | Standard values |
| **Dice** | `ord(c) - 0x2680 + 1` | 1 to 6 |
| **Dominoes** | `left, right = divmod(ord(c) - 0x1F063, 7)` | `left + right` |
| **Mahjong** | Bamboo `0x1F010..`, Chars `0x1F007..`, Dots `0x1F019..` | Tile rank 1 to 9 |
| **Cards** | Ace=1, 2..10=rank, Jack/Queen/King=10 | Card value |

---

## 4. Pathfinding with Dijkstra

Because edge weights are non-negative ($1 + \text{weight}(v) \ge 1$), Dijkstra's algorithm finds the optimal path in $O((V + E) \log V)$ time. On an 11×11 grid ($V \le 121$), Dijkstra executes in under **0.5 milliseconds**!

```python
pq = [(initial_cost, start_r, start_c)]
while pq:
    cost, r, c = heapq.heappop(pq)
    if (r, c) == target:
        break
    for move, (dr, dc) in DIRECTIONS.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < 11 and 0 <= nc < 11 and grid[(nr, nc)] != '#':
            nxt_cost = cost + 1 + get_piece_cost(grid[(nr, nc)])
            if nxt_cost < dist.get((nr, nc), float('inf')):
                dist[(nr, nc)] = nxt_cost
                parent[(nr, nc)] = ((r, c), move)
                heapq.heappush(pq, (nxt_cost, nr, nc))
```

---

## 5. Trap 5: The FIGlet Typography Ambiguity

After clearing round 100/100, the server prints the victory banner using the standard FIGlet font.

In standard FIGlet:
```text
  ___  
 / _ \ 
| | | |
| |_| |
 \___/ 
```
The uppercase letter **`O`** and the digit **`0`** render with **100% identical ASCII glyphs**!

Examining the flag:
`Securinets{d3sp1t3_all_???_rag3_w3_ar3_all_ju5t_rat5_1n_a_maz3}`

The challenge banner includes the hint:
> *"Despite all our rage, we're all just rats in a maze."*

This is the famous lyric from the Smashing Pumpkins song *Bullet with Butterfly Wings*.
The word is `"our"`, which in leetspeak/case formatting is **`OuR`** (Capital O, lowercase u, Capital R).

Submitting the case-sensitive string gives the confirmed flag:
**`Securinets{d3sp1t3_all_OuR_rag3_w3_ar3_all_ju5t_rat5_1n_a_maz3}`**
