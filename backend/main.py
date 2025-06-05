from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
import uuid
import time
from pathlib import Path

# from utils.tracking import process_video

app = FastAPI()

# Setup CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://scaling-space-pancake-wrr9qvr5rq5539p7-5173.app.github.dev"],  # In production, specify exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("static/processed")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Mount static directory to serve processed videos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store job status
job_status = {}

async def process_video_task(input_path, output_path, job_id):
    try:
        job_status[job_id] = {"status": "processing", "progress": 0}
        # process_video(input_path, output_path, job_id)
        job_status[job_id] = {"status": "completed", "progress": 100, "output_url": f"/static/processed/{os.path.basename(output_path)}"}
    except Exception as e:
        job_status[job_id] = {"status": "failed", "error": str(e)}


@app.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    input_filename = f"{job_id}{file_extension}"
    output_filename = f"{job_id}_output.mp4"
    
    input_path = os.path.join(UPLOAD_DIR, input_filename)
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Save uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process video in background
    background_tasks.add_task(process_video_task, input_path, output_path, job_id)
    
    return {"job_id": job_id, "message": "Video upload successful, processing started"}


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_status[job_id]


@app.get("/")
async def root():
    return {"message": "Cup Tracking API"}


# Update progress for a job (called from the tracking module)
def update_progress(job_id, progress):
    if job_id in job_status:
        job_status[job_id]["progress"] = progress 