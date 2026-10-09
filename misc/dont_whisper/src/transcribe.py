"""Speech-to-text helper for the Don't Whisper challenge.

Called by chatapp/app.py as:
    python3 transcribe.py --model tiny.en <audio_path> --language English --best_of 5 --beam_size None

Prints only the transcription on stdout. Uses the openai-whisper package; the
tiny.en model is downloaded into the image at build time (see Dockerfile).
"""
import argparse
import sys


def opt_int(value):
    return None if value in (None, "None", "none", "") else int(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio")
    parser.add_argument("--model", default="tiny.en")
    parser.add_argument("--language", default="English")
    parser.add_argument("--best_of", type=opt_int, default=5)
    parser.add_argument("--beam_size", type=opt_int, default=None)
    args = parser.parse_args()

    import whisper  # openai-whisper

    model = whisper.load_model(args.model, device="cpu")
    result = model.transcribe(
        args.audio,
        language=args.language,
        best_of=args.best_of,
        beam_size=args.beam_size,
        fp16=False,
    )
    print(result.get("text", "").strip())


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # keep the web app's error path simple
        print(f"transcription failed: {exc}", file=sys.stderr)
        sys.exit(1)
