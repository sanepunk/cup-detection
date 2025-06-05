# Cup Tracking Application

This application uses computer vision to track cups in videos. It consists of a FastAPI backend for video processing and a React frontend for uploading videos and viewing the results.

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```
   python start.py
   ```

The backend will run on http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required npm packages:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm run dev
   ```

The frontend will run on http://localhost:5173

## How to Use

1. Open your browser and go to http://localhost:5173
2. Click "Choose Video File" to select a video file
3. Click "Upload and Process" to upload the video and start processing
4. The progress bar will show the processing progress
5. Once processing is complete, the processed video will be displayed

## Features

- Upload video files
- Real-time progress tracking
- Cup detection with bounding boxes
- Responsive UI

## Technologies Used

- Backend:
  - FastAPI
  - OpenCV
  - PyTorch with YOLOv5
  - UVicorn

- Frontend:
  - React
  - Vite
  - CSS

## Directory Structure

```
cupify/
├── backend/
│   ├── utils/
│   │   └── tracking.py
│   ├── main.py
│   ├── start.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```

![Cup Detection Demo](https://github.com/sanepunk/cup-detection/raw/refs/heads/main/Output.mp4)
