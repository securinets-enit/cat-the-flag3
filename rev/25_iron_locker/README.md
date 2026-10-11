# Iron Locker

**Category:** Reverse engineering  
**Difficulty:** Hard  
**Attachment:** `attachments/iron_locker_source/`

Iron Locker is an original Android/WebView/JNI reversing challenge inspired
by the general class of native WebView exploitation tasks. It is not a copy
of any existing challenge.

The application exposes a small JavaScript bridge to a native library. The
bridge manages short-lived locker entries. A lifetime bug in the native
implementation allows a JavaScript payload to read a stale entry after the
allocator reuses its storage. The leaked record contains an encoded recovery
blob rather than the flag itself.

Players must:

1. Trace the JavaScript bridge into JNI.
2. Identify the stale-handle lifetime bug.
3. Trigger the reuse sequence from JavaScript.
4. Parse the leaked record.
5. Reverse the index-dependent byte transform.
6. Verify the recovered flag.

The distributed source is intentionally readable and reproducible. The
Dockerfile prepares a portable analysis environment; an Android SDK/NDK is
required if you want to produce an APK. Keep `src/`, `solver/`, and the flag
file private during the event. The walkthrough is provided separately for
organizers.
