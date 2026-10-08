"""
SecurinetsENIT CTF 2026 - Misc Challenge: Captcha: Rats in a Maze
Author: MrXFuji

Piece definition and cost valuation model.
Base movement onto a tile costs: 1 + piece_value (0 if tile is empty).
"""

import unicodedata

# 1. Chess Pieces (Pawn: 1, Knight: 3, Bishop: 3, Rook: 5, Queen: 9, King: 100)
CHESS_PIECES = {
    # White pieces
    '\u2659': 1,    # ♙ White Pawn
    '\u2658': 3,    # ♘ White Knight
    '\u2657': 3,    # ♗ White Bishop
    '\u2656': 5,    # ♖ White Rook
    '\u2655': 9,    # ♕ White Queen
    '\u2654': 100,  # ♔ White King
    # Black pieces
    '\u265F': 1,    # ♟ Black Pawn
    '\u265E': 3,    # ♞ Black Knight
    '\u265D': 3,    # ♝ Black Bishop
    '\u265C': 5,    # ♜ Black Rook
    '\u265B': 9,    # ♛ Black Queen
    '\u265A': 100,  # ♚ Black King
}

# 2. Dice (U+2680 to U+2685 => values 1 to 6)
# ⚀ ⚁ ⚂ ⚃ ⚄ ⚅
def get_dice_cost(char: str):
    cp = ord(char)
    if 0x2680 <= cp <= 0x2685:
        return cp - 0x2680 + 1
    return None

# 3. Dominoes (Horizontal dominoes from U+1F063 to U+1F08F)
# Formula: left, right = divmod(ord(piece) - 0x1F063, 7); cost = left + right
def get_domino_cost(char: str):
    cp = ord(char)
    if 0x1F063 <= cp <= 0x1F08F:
        left, right = divmod(cp - 0x1F063, 7)
        return left + right
    return None

# 4. Mahjong Tiles (Bamboo: U+1F010..U+1F018, Characters: U+1F007..U+1F00F, Dots: U+1F019..U+1F021)
def get_mahjong_cost(char: str):
    cp = ord(char)
    # Bamboo 1-9
    if 0x1F010 <= cp <= 0x1F018:
        return cp - 0x1F010 + 1
    # Characters 1-9
    if 0x1F007 <= cp <= 0x1F00F:
        return cp - 0x1F007 + 1
    # Circles/Dots 1-9
    if 0x1F019 <= cp <= 0x1F021:
        return cp - 0x1F019 + 1
    return None

# 5. Playing Cards (U+1F0A1 to U+1F0DE)
# Ace = 1, 2..10 = face value, Jack/Queen/King = 10
def get_card_cost(char: str):
    cp = ord(char)
    # Suits: Spades (0x1F0A0), Hearts (0x1F0B0), Diamonds (0x1F0C0), Clubs (0x1F0D0)
    for suit_base in (0x1F0A0, 0x1F0B0, 0x1F0C0, 0x1F0D0):
        if suit_base + 1 <= cp <= suit_base + 0xE:
            rank = cp - suit_base
            if rank == 1:  # Ace
                return 1
            elif 2 <= rank <= 10:
                return rank
            elif rank in (11, 12, 13, 14):  # Jack, Knight, Queen, King
                return 10
    return None

def get_piece_cost(char: str) -> int:
    """Returns the piece weight value (0 if not a piece)."""
    if not char or char in (' ', '·', '#', '█'):
        return 0

    if char in CHESS_PIECES:
        return CHESS_PIECES[char]

    dice = get_dice_cost(char)
    if dice is not None:
        return dice

    domino = get_domino_cost(char)
    if domino is not None:
        return domino

    mahjong = get_mahjong_cost(char)
    if mahjong is not None:
        return mahjong

    card = get_card_cost(char)
    if card is not None:
        return card

    return 0

def is_wide_character(char: str) -> bool:
    """
    Checks if a character occupies 2 columns in standard terminal emulators.
    Unicode East Asian Width (UAX #11):
    'W' (Wide) or 'F' (Fullwidth) take 2 terminal columns.
    Many emoji and symbols in supplementary planes (U+1F000+) are rendered wide.
    """
    cp = ord(char)
    # Dominoes, Mahjong, Playing Cards all reside in U+1F000..U+1F0FF
    if 0x1F000 <= cp <= 0x1F0FF:
        return True
    return unicodedata.east_asian_width(char) in ('W', 'F')

# Pool of available pieces for maze generation
ALL_PIECES_SAMPLE = []
# Chess
ALL_PIECES_SAMPLE.extend(list(CHESS_PIECES.keys()))
# Dice (1..6)
ALL_PIECES_SAMPLE.extend([chr(0x2680 + i) for i in range(6)])
# Selected Dominoes
ALL_PIECES_SAMPLE.extend([chr(0x1F063 + i) for i in range(49)])
# Selected Mahjong (Bamboo 1..9, Chars 1..9, Dots 1..9)
ALL_PIECES_SAMPLE.extend([chr(0x1F010 + i) for i in range(9)])
ALL_PIECES_SAMPLE.extend([chr(0x1F007 + i) for i in range(9)])
ALL_PIECES_SAMPLE.extend([chr(0x1F019 + i) for i in range(9)])
# Selected Playing Cards (Spades & Hearts)
ALL_PIECES_SAMPLE.extend([chr(0x1F0A1 + i) for i in range(14) if i != 11])
ALL_PIECES_SAMPLE.extend([chr(0x1F0B1 + i) for i in range(14) if i != 11])
