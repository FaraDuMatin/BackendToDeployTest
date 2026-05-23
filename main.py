import os
import tempfile
import uuid
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class DownloadRequest(BaseModel):
    url: str

def cleanup_file(filepath: str):
    """Deletes the temporary file after it has been sent to the user."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Cleaned up {filepath}")
    except Exception as e:
        print(f"Failed to delete {filepath}: {e}")

@app.post("/api/download")
async def download_youtube_video(request: DownloadRequest, background_tasks: BackgroundTasks):
    url = request.url
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # Generate a unique ID to prevent conflicts when multiple users download at once
    file_id = str(uuid.uuid4())
    temp_dir = tempfile.gettempdir()
    
    # We ask yt-dlp to save the file using this naming template
    output_template = os.path.join(temp_dir, f"{file_id}.%(ext)s")
    final_filepath = os.path.join(temp_dir, f"{file_id}.mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # 192 kbps is a great balance of size and quality
        }],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # Execute the download and conversion
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"yt-dlp error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process video.")

    if not os.path.exists(final_filepath):
        raise HTTPException(status_code=500, detail="Output file not found after conversion.")

    # Schedule the file to be deleted right after the HTTP response completes
    background_tasks.add_task(cleanup_file, final_filepath)

    # Stream the file back to the client
    return FileResponse(
        path=final_filepath,
        media_type="audio/mpeg",
        filename="download.mp3"
    )