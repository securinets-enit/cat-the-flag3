# Don't Whisper

**Category:** Misc
**Author:** MrXFuji
**Difficulty:** Medium

## Description (for CTFd)

Our new AI buddy loves to chat. Type to it, or send it a voice message and it
will listen carefully to every word you say.

Just be careful what you whisper.

**Connection:** `http://<host>:8005`

## Files given to players

None. Players only get the URL.

## Deployment

```bash
cd misc/dont_whisper/src
docker build -t dont-whisper .
docker run -d -p 8005:8005 --name dont-whisper dont-whisper
```

The build downloads CPU PyTorch and the Whisper `tiny.en` speech model once,
so the build machine needs internet. The running container does not.

The flag lives at `/chal/flag` inside the container.

## Organizer notes (do not publish)

- **Text chat (`/api/chat`)** is safe: the message goes through
  `sanitize_input()` and is passed to `chatbot.py` as a list argument, with no
  shell involved.
- **Voice chat (`/api/audio-chat`)** is the bug. The audio is transcribed by
  Whisper, and the transcription is pasted, unsanitized, into a shell command:

  ```python
  asyncio.create_subprocess_shell(f"python3 chatbot.py '{transcription}'", ...)
  ```

  stdout and stderr of that shell are returned to the player in the
  `response` field. A transcription containing a `'` closes the quote and
  everything after it runs as shell commands.
- The intended solve is to craft or record audio whose transcription breaks
  out of the quotes and reads `/chal/flag`, for example by using
  text-to-speech and iterating on the wording until Whisper outputs the
  characters you need.

**Before publishing:** the original author (MrXFuji) should confirm the
intended payload, build the image once, and run the solve against it. The
speech-to-text helper (`transcribe.py`) was rebuilt from the call in `app.py`
because the original `whisper.py`, `whisper/` folder and model file were
missing from the repo.

## Flag

See `src/flag`.
