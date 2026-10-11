# Thermal Tumble

**Category:** Misc  
**Difficulty:** Intermediate–Hard  
**Attachment:** `attachments/index.html`

Thermal Tumble is an original browser puzzle inspired by GPU-assisted
parameter-search challenges. The page displays a harmless animated canvas,
but the useful result is written into a hidden pixel buffer only for one
cycle/temperature pair.

Players must:

1. Read the bundled JavaScript and identify the parameter ranges.
2. Understand the seed and acceptance predicate.
3. Search the finite parameter space.
4. Extract the hidden RGBA pixels rather than relying on the visible canvas.
5. Undo the per-byte XOR transform and validate the flag.

The challenge is offline and needs only a modern browser or Python 3.8+ for
the supplied solver. Keep `src/`, `solver/`, and the flag file private during
the event.
