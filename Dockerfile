# Use the official lightweight Python image
FROM python:3.11-slim

# Install FFmpeg (CRITICAL: yt-dlp requires this to extract MP3)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port (Render sets the PORT environment variable dynamically)
EXPOSE 8000

# Start the FastAPI app. We use Render's dynamic $PORT or fallback to 8000.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}