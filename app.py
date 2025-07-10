
# from flask import Flask, render_template, request, Response
# import os
# import cv2
# import uuid
# import datetime
# import json
# import numpy as np
# from pymongo import MongoClient
# from urllib.parse import quote_plus
# from insightface.app import FaceAnalysis
# from deep_sort_realtime.deepsort_tracker import DeepSort

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'static/output'
# LOG_JSON = 'face_tracking_logs.json'

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # === MongoDB Atlas Configuration ===
# username = quote_plus("22ad062")
# password = quote_plus("Student@123")
# mongo_uri = f"mongodb+srv://{username}:{password}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"
# client = MongoClient(mongo_uri)
# db = client["face_tracker"]
# logs_col = db["tracking_logs"]

# # === Load High-Accuracy InsightFace Model (GPU Optimized) ===
# face_model = FaceAnalysis(name="antelopev2", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# #face_model = FaceAnalysis(name="antelopev2", providers=['CPUExecutionProvider'])
# face_model.prepare(ctx_id=0)

# # === DeepSORT Tracker ===
# tracker = DeepSort(max_age=30)

# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/upload_stream', methods=["POST"])
# def upload_stream():
#     file = request.files['video']
#     filename = f"{uuid.uuid4().hex}_{file.filename}"
#     input_path = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(input_path)
#     return render_template("stream.html", stream_url=f"/stream_video/{filename}")

# @app.route('/stream_video/<filename>')
# def stream_video(filename):
#     input_path = os.path.join(UPLOAD_FOLDER, filename)
#     return Response(
#         process_stream(input_path, source_type="video", source_name=filename),
#         mimetype='multipart/x-mixed-replace; boundary=frame'
#     )

# @app.route('/webcam')
# def webcam():
#     return render_template("stream.html", stream_url="/stream_webcam")

# @app.route('/stream_webcam')
# def stream_webcam():
#     return Response(
#         process_stream(0, source_type="webcam", source_name="live"),
#         mimetype='multipart/x-mixed-replace; boundary=frame'
#     )

# def process_stream(source, source_type, source_name):
#     cap = cv2.VideoCapture(source)
#     frame_rate = cap.get(cv2.CAP_PROP_FPS) or 25
#     frame_idx = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_idx += 1
#         timestamp = frame_idx / frame_rate
#         faces = face_model.get(frame)
#         detections = []

#         for face in faces:
#             x1, y1, x2, y2 = face.bbox.astype(int)
#             detections.append(([x1, y1, x2 - x1, y2 - y1], 0.99, "face"))

#         tracks = tracker.update_tracks(detections, frame=frame)

#         for track in tracks:
#             if not track.is_confirmed():
#                 continue

#             track_id = track.track_id
#             l, t, w, h = track.to_ltrb()
#             x1, y1, x2, y2 = map(int, [l, t, l + w, t + h])

#             # Skip invalid crops
#             if x1 >= x2 or y1 >= y2 or x2 > frame.shape[1] or y2 > frame.shape[0]:
#                 continue

#             # Draw box and label
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#             # Save cropped face
#             face_crop = frame[y1:y2, x1:x2]
#             try:
#                 _, buffer = cv2.imencode('.jpg', face_crop)

#                 # === MongoDB Logging ===
#                 logs_col.insert_one({
#                     "track_id": track_id,
#                     "timestamp": datetime.datetime.now(),
#                     "source": source_type,
#                     "source_name": source_name,
#                     "bbox": [x1, y1, x2, y2],
#                     "frame_number": frame_idx,
#                     "video_time": timestamp,
#                     "face_image": buffer.tobytes()
#                 })

#                 # === JSON Logging ===
#                 log_entry = {
#                     "track_id": track_id,
#                     "source": source_type,
#                     "source_name": source_name,
#                     "timestamp": datetime.datetime.now().isoformat(),
#                     "video_time": f"{timestamp:.2f}s",
#                     "bbox": [x1, y1, x2, y2]
#                 }
#                 with open(LOG_JSON, "a") as f:
#                     f.write(json.dumps(log_entry) + "\n")
#             except Exception as e:
#                 print(f"⚠️ MongoDB insert error: {e}")

#         _, jpeg = cv2.imencode('.jpg', frame)
#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' +
#                jpeg.tobytes() + b'\r\n')

#     cap.release()

# @app.route('/logs')
# def logs():
#     entries = logs_col.find().sort("timestamp", -1).limit(50)
#     return render_template("logs.html", logs=entries)

# if __name__ == '__main__':
#     app.run(debug=True, threaded=True)



from flask import Flask, render_template, request, Response
import os, cv2, uuid, datetime, json
import numpy as np
from urllib.parse import quote_plus
from pymongo import MongoClient
from insightface.app import FaceAnalysis
from deep_sort_realtime.deepsort_tracker import DeepSort

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
LOG_JSON = 'face_tracking_logs.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === MongoDB Atlas Configuration ===
DB_USERNAME = quote_plus("22ad062")
DB_PASSWORD = quote_plus("Student@123")
MONGO_URI = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"

client = MongoClient(MONGO_URI)
db = client["face_tracker"]
logs_col = db["tracking_logs"]

# === InsightFace Model (buffalo_l for better accuracy) ===
face_model = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
face_model.prepare(ctx_id=0)

# === DeepSORT Tracker ===
tracker = DeepSort(max_age=30)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload_stream', methods=["POST"])
def upload_stream():
    file = request.files['video']
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    return render_template("stream.html", stream_url=f"/stream_video/{filename}")

@app.route('/stream_video/<filename>')
def stream_video(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return Response(process_stream(path, "video", filename),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam')
def webcam():
    return render_template("stream.html", stream_url="/stream_webcam")

@app.route('/stream_webcam')
def stream_webcam():
    return Response(process_stream(0, "webcam", "live"),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def process_stream(source, source_type, source_name):
    cap = cv2.VideoCapture(source)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        timestamp = frame_idx / fps
        faces = face_model.get(frame)
        detections = []

        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)
            detections.append(([x1, y1, x2 - x1, y2 - y1], 0.99, "face"))

        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, w, h = track.to_ltrb()
            x1, y1, x2, y2 = map(int, [l, t, l + w, t + h])

            # Skip invalid crops
            if y2 <= y1 or x2 <= x1:
                continue

            # Draw box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            try:
                face_crop = frame[y1:y2, x1:x2]
                _, buffer = cv2.imencode('.jpg', face_crop)

                # MongoDB Logging
                logs_col.insert_one({
                    "track_id": track_id,
                    "timestamp": datetime.datetime.now(),
                    "source": source_type,
                    "source_name": source_name,
                    "frame_number": frame_idx,
                    "video_time": timestamp,
                    "bbox": [x1, y1, x2, y2],
                    "face_image": buffer.tobytes()
                })

                # Local JSON logging
                log_entry = {
                    "track_id": track_id,
                    "source": source_type,
                    "source_name": source_name,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "video_time": f"{timestamp:.2f}s",
                    "bbox": [x1, y1, x2, y2]
                }
                with open(LOG_JSON, "a") as f:
                    f.write(json.dumps(log_entry) + "\n")

            except Exception as e:
                print(f"⚠️ MongoDB insert error: {e}")

        # Stream output
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' +
               jpeg.tobytes() + b'\r\n')

    cap.release()

@app.route('/logs')
def logs():
    entries = logs_col.find().sort("timestamp", -1).limit(50)
    return render_template("logs.html", logs=entries)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
