Iron Locker source attachment.

The Java and native sources intentionally expose the complete JNI boundary.
Build notes are in build_notes.txt. The native implementation uses a
deterministic one-slot pool so the stale-handle behavior is reproducible.
