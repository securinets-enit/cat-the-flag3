"""
SecurinetsENIT CTF 2026 - Misc Challenge: Captcha: Rats in a Maze
Author: MrXFuji

Maze generator with:
- 11x11 interior grid
- Outer borders with ANSI Green Entrance & ANSI Red Exit
- Board-game pieces on tiles with compact cost valuation
- Double-width terminal formatting (East Asian Width 2 columns per cell)
- Guaranteed strictly unique Dijkstra minimum-cost path
"""

import random
import heapq
from pieces import (
    ALL_PIECES_SAMPLE,
    get_piece_cost,
    is_wide_character
)

ANSI_RESET  = "\x1b[0m"
ANSI_GREEN  = "\x1b[92m"  # Entrance
ANSI_RED    = "\x1b[91m"  # Exit
ANSI_WALL   = "\x1b[36m"  # Cyan wall
ANSI_BOLD   = "\x1b[1m"

DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}
OPPOSITE = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}

class Maze:
    def __init__(self, size=11):
        self.size = size  # 11x11 interior
        self.grid = {}    # (r, c) -> char ('#' for wall, '·' for empty, or piece)
        self.enter_side = None   # 'T', 'B', 'L', 'R'
        self.enter_pos = None    # (r, c) in interior
        self.enter_dir = None    # 'D', 'U', 'R', 'L'
        self.exit_side = None    # 'T', 'B', 'L', 'R'
        self.exit_pos = None     # (r, c) in interior
        self.exit_dir = None     # 'D', 'U', 'R', 'L'
        self.solution_moves = None
        self.solution_cost = None

    def generate(self):
        while True:
            if self._try_generate():
                break

    def _try_generate(self):
        # Initialize grid with walls
        grid = {}
        for r in range(self.size):
            for c in range(self.size):
                grid[(r, c)] = '#'

        # Generate spanning tree on odd cells (r%2==0, c%2==0) using randomized DFS
        nodes = [(r, c) for r in range(0, self.size, 2) for c in range(0, self.size, 2)]
        visited = set()
        stack = [nodes[0]]
        visited.add(nodes[0])
        grid[nodes[0]] = '·'

        while stack:
            curr = stack[-1]
            neighbors = []
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and (nr, nc) not in visited:
                    neighbors.append(((nr, nc), (curr[0] + dr // 2, curr[1] + dc // 2)))
            if neighbors:
                nxt, wall = random.choice(neighbors)
                visited.add(nxt)
                grid[nxt] = '·'
                grid[wall] = '·'
                stack.append(nxt)
            else:
                stack.pop()

        # Add some random cycles so there are multiple paths with different costs
        extra_openings = random.randint(8, 14)
        for _ in range(extra_openings):
            wr = random.randint(0, self.size - 1)
            wc = random.randint(0, self.size - 1)
            if grid[(wr, wc)] == '#':
                # Open if adjacent to at least two open cells
                adj = 0
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if (wr + dr, wc + dc) in grid and grid[(wr + dr, wc + dc)] != '#':
                        adj += 1
                if adj >= 2:
                    grid[(wr, wc)] = '·'

        # Pick Entrance and Exit on borders
        # Entrance on Top or Left border, Exit on Bottom or Right border
        if random.random() < 0.5:
            # Entrance on Top (row 0), enters with 'D'
            valid_cols = [c for c in range(self.size) if grid[(0, c)] != '#']
            if not valid_cols:
                return False
            enter_c = random.choice(valid_cols)
            enter_side = 'T'
            enter_pos = (0, enter_c)
            enter_dir = 'D'
        else:
            # Entrance on Left (col 0), enters with 'R'
            valid_rows = [r for r in range(self.size) if grid[(r, 0)] != '#']
            if not valid_rows:
                return False
            enter_r = random.choice(valid_rows)
            enter_side = 'L'
            enter_pos = (enter_r, 0)
            enter_dir = 'R'

        if random.random() < 0.5:
            # Exit on Bottom (row size-1), exits with 'D'
            valid_cols = [c for c in range(self.size) if grid[(self.size - 1, c)] != '#']
            if not valid_cols:
                return False
            exit_c = random.choice(valid_cols)
            exit_side = 'B'
            exit_pos = (self.size - 1, exit_c)
            exit_dir = 'D'
        else:
            # Exit on Right (col size-1), exits with 'R'
            valid_rows = [r for r in range(self.size) if grid[(r, self.size - 1)] != '#']
            if not valid_rows:
                return False
            exit_r = random.choice(valid_rows)
            exit_side = 'R'
            exit_pos = (exit_r, self.size - 1)
            exit_dir = 'R'

        if enter_pos == exit_pos:
            return False

        # Place pieces on walkable tiles (probability ~ 45%)
        for (r, c), val in list(grid.items()):
            if val == '·':
                if random.random() < 0.45:
                    grid[(r, c)] = random.choice(ALL_PIECES_SAMPLE)

        # Check unique Dijkstra
        self.grid = grid
        self.enter_side = enter_side
        self.enter_pos = enter_pos
        self.enter_dir = enter_dir
        self.exit_side = exit_side
        self.exit_pos = exit_pos
        self.exit_dir = exit_dir

        is_unique, cost, moves = self._solve_dijkstra()
        if not is_unique:
            # Attempt to break ties by randomly modifying a piece on an open cell
            for _ in range(10):
                r = random.randint(0, self.size - 1)
                c = random.randint(0, self.size - 1)
                if self.grid[(r, c)] != '#':
                    self.grid[(r, c)] = random.choice(ALL_PIECES_SAMPLE)
                    is_unique, cost, moves = self._solve_dijkstra()
                    if is_unique:
                        break
            if not is_unique:
                return False

        self.solution_cost = cost
        self.solution_moves = moves
        return True

    def _solve_dijkstra(self):
        """
        Solves the maze using Dijkstra's algorithm.
        Returns (is_unique, min_cost, moves_string).
        Cost model:
          Entering cell v costs 1 + weight(v).
          First move enters self.enter_pos with cost 1 + weight(self.enter_pos).
          Final move leaves self.exit_pos to outer border with cost 1.
        """
        start_node = self.enter_pos
        target_node = self.exit_pos

        # dist[(r, c)] = (min_cost, path_moves)
        dist = {}
        ways = {} # ways[(r, c)] = number of shortest paths reaching (r, c)
        
        initial_cost = 1 + get_piece_cost(self.grid[start_node])
        dist[start_node] = initial_cost
        ways[start_node] = 1

        # Priority queue: (cost, r, c, moves)
        pq = [(initial_cost, start_node[0], start_node[1], self.enter_dir)]

        while pq:
            cost, r, c, moves = heapq.heappop(pq)

            if cost > dist.get((r, c), float('inf')):
                continue

            if (r, c) == target_node:
                # Target reached. Check if reached with minimum cost.
                continue

            for m, (dr, dc) in DIRECTIONS.items():
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if self.grid[(nr, nc)] != '#':
                        edge_cost = 1 + get_piece_cost(self.grid[(nr, nc)])
                        new_cost = cost + edge_cost
                        if (nr, nc) not in dist or new_cost < dist[(nr, nc)]:
                            dist[(nr, nc)] = new_cost
                            ways[(nr, nc)] = ways.get((r, c), 1)
                            heapq.heappush(pq, (new_cost, nr, nc, moves + m))
                        elif new_cost == dist[(nr, nc)]:
                            ways[(nr, nc)] = ways.get((nr, nc), 0) + ways.get((r, c), 1)

        if target_node not in dist:
            return False, None, None

        # Add exit move cost: +1
        final_cost = dist[target_node] + 1
        final_moves = None
        # Retrieve the moves string from the priority pop
        # Run standard Dijkstra to get exact path
        parent = {}
        p_dist = {start_node: initial_cost}
        q = [(initial_cost, start_node[0], start_node[1])]
        while q:
            c_cost, cr, cc = heapq.heappop(q)
            if c_cost > p_dist[(cr, cc)]:
                continue
            if (cr, cc) == target_node:
                break
            for m, (dr, dc) in DIRECTIONS.items():
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[(nr, nc)] != '#':
                    nxt_cost = c_cost + 1 + get_piece_cost(self.grid[(nr, nc)])
                    if (nr, nc) not in p_dist or nxt_cost < p_dist[(nr, nc)]:
                        p_dist[(nr, nc)] = nxt_cost
                        parent[(nr, nc)] = ((cr, cc), m)
                        heapq.heappush(q, (nxt_cost, nr, nc))

        # Reconstruct moves
        curr = target_node
        path_moves = []
        while curr != start_node:
            p_node, m = parent[curr]
            path_moves.append(m)
            curr = p_node
        path_moves.reverse()

        full_moves = self.enter_dir + "".join(path_moves) + self.exit_dir
        is_unique = (ways.get(target_node, 0) == 1)
        return is_unique, final_cost, full_moves

    def render_terminal(self) -> str:
        """
        Renders the maze into an ANSI-escaped terminal string.
        Every visual cell takes exactly 2 terminal columns:
          - Wall '#' is rendered as ANSI_WALL + '# ' + ANSI_RESET (2 display columns)
          - Empty '·' is rendered as '· ' (2 display columns)
          - Narrow pieces (chess, dice) rendered as 'P ' (2 display columns)
          - Wide pieces (domino, mahjong, card) rendered as 'W' (2 display columns)
          - Entrance border segment is ANSI_GREEN + '══' + ANSI_RESET
          - Exit border segment is ANSI_RED + '══' + ANSI_RESET
        """
        lines = []

        # Top border
        top_cells = []
        top_cells.append(ANSI_WALL + "╔═" + ANSI_RESET)
        for c in range(self.size):
            if self.enter_side == 'T' and self.enter_pos[1] == c:
                top_cells.append(ANSI_GREEN + "══" + ANSI_RESET)
            elif self.exit_side == 'T' and self.exit_pos[1] == c:
                top_cells.append(ANSI_RED + "══" + ANSI_RESET)
            else:
                top_cells.append(ANSI_WALL + "══" + ANSI_RESET)
        top_cells.append(ANSI_WALL + "╗" + ANSI_RESET)
        lines.append("".join(top_cells))

        # Interior rows
        for r in range(self.size):
            row_cells = []
            # Left border for this row
            if self.enter_side == 'L' and self.enter_pos[0] == r:
                row_cells.append(ANSI_GREEN + "║ " + ANSI_RESET)
            elif self.exit_side == 'L' and self.exit_pos[0] == r:
                row_cells.append(ANSI_RED + "║ " + ANSI_RESET)
            else:
                row_cells.append(ANSI_WALL + "║ " + ANSI_RESET)

            # Grid cells
            for c in range(self.size):
                ch = self.grid[(r, c)]
                if ch == '#':
                    row_cells.append(ANSI_WALL + "# " + ANSI_RESET)
                elif ch == '·':
                    row_cells.append("· ")
                else:
                    if is_wide_character(ch):
                        # Wide character takes 2 terminal columns itself!
                        row_cells.append(ch)
                    else:
                        # Narrow character takes 1 column, append 1 space
                        row_cells.append(ch + " ")

            # Right border for this row
            if self.enter_side == 'R' and self.enter_pos[0] == r:
                row_cells.append(ANSI_GREEN + "║" + ANSI_RESET)
            elif self.exit_side == 'R' and self.exit_pos[0] == r:
                row_cells.append(ANSI_RED + "║" + ANSI_RESET)
            else:
                row_cells.append(ANSI_WALL + "║" + ANSI_RESET)

            lines.append("".join(row_cells))

        # Bottom border
        bot_cells = []
        bot_cells.append(ANSI_WALL + "╚═" + ANSI_RESET)
        for c in range(self.size):
            if self.enter_side == 'B' and self.enter_pos[1] == c:
                bot_cells.append(ANSI_GREEN + "══" + ANSI_RESET)
            elif self.exit_side == 'B' and self.exit_pos[1] == c:
                bot_cells.append(ANSI_RED + "══" + ANSI_RESET)
            else:
                bot_cells.append(ANSI_WALL + "══" + ANSI_RESET)
        bot_cells.append(ANSI_WALL + "╝" + ANSI_RESET)
        lines.append("".join(bot_cells))

        return "\n".join(lines) + "\n"
