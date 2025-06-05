import cv2
import torch
import os
import sys

# Add the parent directory to the path to import update_progress
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from main import update_progress
except ImportError:
    # Mock function in case we're running this directly
    def update_progress(job_id, progress):
        print(f"Progress: {progress}%")

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

TARGET_CLASS = 'cup'

input_video_path = '/workspaces/coffee-mug-tracker-ops/uploads/6202068-sd_640_360_24fps.mp4'
output_video_path = '/workspaces/coffee-mug-tracker-ops/static/processed/output.mp4'

def process_video(input_video_path, output_video_path, job_id=None):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {input_video_path}")
        raise Exception(f"Unable to open video file {input_video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    print("Processing video for cup detection...")
    
    frame_count = 0
    last_progress = -1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections = results.pandas().xyxy[0]

        cups = detections[detections['name'] == TARGET_CLASS]

        for _, row in cups.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            confidence = row['confidence']

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{TARGET_CLASS} {confidence:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        out.write(frame)
        
        # Update progress
        frame_count += 1
        progress = min(int((frame_count / total_frames) * 100), 100)
        
        # Only update when progress changes by at least 1%
        if progress != last_progress and job_id:
            update_progress(job_id, progress)
            last_progress = progress

    cap.release()
    out.release()
    
    print(f"Finished processing. Output saved to {output_video_path}")
    return output_video_path
