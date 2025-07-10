# Intelligent Face Tracker with Auto-Registration and MongoDB Atlas Logging

This project is a real-time face detection, tracking, and registration system built using:

- YOLO / InsightFace for face detection and recognition
- DeepSORT for face tracking
- Flask for backend web server
- MongoDB Atlas for cloud-based logging
- JSON file for local backup logging
- GPU acceleration with ONNX Runtime (CUDAExecutionProvider)

---

## Key Features

- Real-time face detection from webcam or uploaded video
- Automatic generation of unique track ID for each detected face
- Logs stored in MongoDB Atlas and locally in `face_tracking_logs.json`
- Uses high-accuracy face embeddings from InsightFace (`antelopev2` model)
- Tracks faces across frames with DeepSORT
- Supports both GPU and CPU execution
- Clean and responsive web interface using Flask

---

## Project Structure

```
face_tracker/
│
├── app.py                        # Main Flask backend
├── test_atlas.py                # MongoDB Atlas connection tester
├── registered_faces/            # Folder to store cropped face images
├── uploads/                     # Uploaded video storage
├── static/output/               # Output processed media
├── templates/
│   ├── index.html               # Home page
│   └── stream.html              # Live stream viewer
├── face_tracking_logs.json      # Local JSON file log
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Step 1: Clone and Install Dependencies

```bash
git clone https://github.com/yourusername/face-tracker.git
cd face-tracker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Ensure:
- Python version 3.10 is installed
- GPU users install `onnxruntime-gpu`

---

## Step 2: MongoDB Atlas Setup

1. Visit: https://cloud.mongodb.com
2. Create a **Free Cluster (M0 Tier)**
3. Create a database user:
   - Username: `22ad062`
   - Password: `Student@123`
4. Add network access: allow from `0.0.0.0/0`
5. Create a database: `face_tracker`
6. Inside the database, create a collection: `tracking_logs`

Update the MongoDB connection string in `app.py`:

```python
from urllib.parse import quote_plus
username = quote_plus("22ad062")
password = quote_plus("Student@123")
mongo_uri = f"mongodb+srv://{username}:{password}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"
```

---

## Step 3: Run the Application

```bash
python app.py
```

Navigate to:

```
http://127.0.0.1:5000/
```

- Use "Upload Video" or "Start Webcam"
- Live face tracking will begin
- Logs are recorded to MongoDB and local JSON

---

## Logging Details

### Stored in MongoDB Atlas

- Track ID (unique identifier per face)
- Timestamp
- Bounding box coordinates
- Video time (in seconds)
- Cropped face image (stored in binary format)

### Stored in Local JSON File

- Same as above, stored in readable `face_tracking_logs.json`

---

## Deployment Instructions (Render)

1. Push the project to GitHub
2. Visit https://render.com
3. Click “New Web Service”
4. Connect GitHub repository
5. Use the following settings:

   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Runtime: Python 3.10

6. Optionally add environment variables:

```
DB_USERNAME = 22ad062
DB_PASSWORD = Student@123
```

After deployment, Render will generate a public URL for access.

---

## Troubleshooting

- **SSL Handshake Failure**:
  - Ensure IP address is added in MongoDB Atlas Network Access
  - Confirm correct username/password in your connection URI

- **Slow Video Playback**:
  - Use the `antelopev2` model
  - Ensure GPU is being utilized with `onnxruntime-gpu`

- **Face Image Not Saving**:
  - Ensure valid coordinates using: `if y2 > y1 and x2 > x1` before cropping
  - Validate image before encoding with OpenCV

---

## Dependencies

```
Flask
opencv-python
deep_sort_realtime
insightface
onnxruntime-gpu
pymongo
numpy
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## Author

YUVASREE P  
Roll No: 22AD062  
Institution: Dr. N.G.P. Institute of Technology  
Email: 22ad062@drngpit.ac.in  
Project Submitted for: Katomaran Hackathon

---

Working video link-https://drive.google.com/file/d/17hTJxiXSl7k43QBhBCplUU_v26rQXs6l/view?usp=sharing

---
## License

This project is open source and available under the MIT License.
