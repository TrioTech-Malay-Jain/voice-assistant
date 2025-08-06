FROM python:3.10

WORKDIR /app

COPY . .

# Install system-level dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run your LiveKit agent script
CMD ["python", "run_livekit_agent.py"]
