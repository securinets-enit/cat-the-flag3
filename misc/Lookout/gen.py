#!/usr/bin/env python3
"""
gen.py — builds a seeded-PRNG XOR challenge instance.

Usage:
    python3 gen.py "MYCTF{your_flag_here}" 8675309
    python3 gen.py "MYCTF{your_flag_here}" --date-hash 2001-09-11
"""
import sys
import random
import json
import hashlib

def derive_seed_from_date(date_str: str) -> int:
    """seed = int(sha256(date_str).hexdigest()[:8], 16)"""
    h = hashlib.sha256(date_str.encode()).hexdigest()
    return int(h[:8], 16)

def make_challenge(flag: str, seed: int, model_name: str, layer_name: str, note: str, seed_hint: str = None):
    flag_bytes = flag.encode()
    r = random.Random(seed)
    mask = bytes(r.randrange(256) for _ in range(len(flag_bytes)))
    cipher = bytes(f ^ m for f, m in zip(flag_bytes, mask))

    result = {
        "model": model_name,
        "reproducibility": "exact",
        "layer": layer_name,
        "mask_algorithm": "python random.Random(seed).randrange(256) per byte",
        "cipher_hex": cipher.hex(),
        "ai_note": note,
    }
    if seed_hint:
        # seed is NOT given directly — must be derived
        result["seed_derivation"] = seed_hint
    else:
        result["seed"] = seed
    return result

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] != "--date-hash":
        flag = sys.argv[1]
        seed = int(sys.argv[2])
        seed_hint = None
    elif len(sys.argv) == 3 and sys.argv[1] == "--date-hash":
        print("Usage: gen.py <flag> --date-hash <YYYY-MM-DD>", file=sys.stderr)
        sys.exit(1)
    elif len(sys.argv) == 4 and sys.argv[2] == "--date-hash":
        flag = sys.argv[1]
        date_str = sys.argv[3]
        seed = derive_seed_from_date(date_str)
        seed_hint = "int(sha256(date_string).hexdigest()[:8], 16), date given as YYYY-MM-DD"
    else:
        print(f"Usage: {sys.argv[0]} <flag> <seed>")
        print(f"       {sys.argv[0]} <flag> --date-hash <YYYY-MM-DD>")
        sys.exit(1)

    challenge = make_challenge(
        flag=flag,
        seed=seed,
        model_name="dream-checkpoint-final-FINAL-v3",
        layer_name="secret_mask_head",
        note="Publishing the seed is safe because random means random.",
        seed_hint=seed_hint,
    )

    print(json.dumps(challenge, indent=2))

