# Slot Pusher

**Category:** Reverse engineering  
**Difficulty:** Hard  
**Attachment:** `attachments/slot_pusher.py`

Slot Pusher is an original, portable challenge inspired by signal-driven
state-machine reversing. The attachment presents a noisy menu loop and keeps
its useful data in a rotating set of stack slots. The visible operations push
literal bytes, rewind selected slots, and finally test the constructed token.

Players must:

1. Recover the slot transition rules.
2. Notice that menu choices are parsed as integers but push values are read as
   single characters.
3. Generate a repeated cycle that leaves one new character live per round.
4. Reach the hidden verification path.
5. Decode the recovered token with the index-dependent transform.

This version is fully offline and runs with Python 3.8+. Keep `src/`, `solver/`,
and the flag file private during the event.
