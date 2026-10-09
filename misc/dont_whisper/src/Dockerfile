# syntax=docker/dockerfile:1

FROM ubuntu:22.04

# Install app dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip gunicorn ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /

# CPU-only torch first, so openai-whisper does not pull the huge CUDA build
RUN pip install --no-cache-dir torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir -r /requirements.txt

# Bake the speech model into the image so the container needs no internet at runtime
RUN python3 -c "import whisper; whisper.load_model('tiny.en', device='cpu')"

COPY chatapp /chatapp
COPY chatbot.py /chatapp
COPY transcribe.py /chatapp/transcribe.py

# Expose port for the app
EXPOSE 8005

# Copy flag file for challenge
COPY flag /chal/flag

# Set working directory for the app
WORKDIR /chatapp

# Start the app with Gunicorn and Uvicorn worker
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8005"]
