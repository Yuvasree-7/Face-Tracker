
# import cv2, os, uuid, datetime
# import numpy as np
# from urllib.parse import quote_plus
# from pymongo import MongoClient
# from insightface.app import FaceAnalysis

# DB_USERNAME = "22ad062"
# DB_PASSWORD = quote_plus("Student@123")
# mongo_uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"

# client = MongoClient(mongo_uri)
# db = client["face_tracker"]
# collection = db["registered_faces"]
# SAVE_DIR = "registered_faces"
# os.makedirs(SAVE_DIR, exist_ok=True)

# app = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
# app.prepare(ctx_id=0)

# cap = cv2.VideoCapture(0)
# print("[INFO] Press SPACE to register face, ESC to exit")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     cv2.imshow("Register", frame)
#     key = cv2.waitKey(1)

#     if key == 27:
#         break
#     elif key == 32:
#         faces = app.get(frame)
#         if not faces:
#             print("No face found.")
#             continue

#         face = faces[0]
#         face_id = str(uuid.uuid4())
#         embedding = face.embedding.tolist()
#         x1, y1, x2, y2 = face.bbox.astype(int)
#         face_img = frame[y1:y2, x1:x2]
#         img_path = os.path.join(SAVE_DIR, f"{face_id}.jpg")
#         cv2.imwrite(img_path, face_img)

#         collection.insert_one({
#             "face_id": face_id,
#             "embedding": embedding,
#             "image_path": img_path,
#             "timestamp": datetime.datetime.now()
#         })
#         print(f"✅ Registered face: {face_id}")

# cap.release()
# cv2.destroyAllWindows()


import cv2, os, uuid, datetime
import numpy as np
from urllib.parse import quote_plus
from pymongo import MongoClient
from insightface.app import FaceAnalysis

# MongoDB connection
DB_USERNAME = "22ad062"
DB_PASSWORD = quote_plus("Student@123")
mongo_uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"
client = MongoClient(mongo_uri)
db = client["face_tracker"]
collection = db["registered_faces"]

# Face storage directory
SAVE_DIR = "registered_faces"
os.makedirs(SAVE_DIR, exist_ok=True)

# Load InsightFace
app = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
app.prepare(ctx_id=0)

# Webcam for face capture
cap = cv2.VideoCapture(0)
print("[INFO] Press SPACE to register face, ESC to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Register", frame)
    key = cv2.waitKey(1)

    if key == 27:
        break
    elif key == 32:
        faces = app.get(frame)
        if not faces:
            print("❌ No face detected.")
            continue

        face = faces[0]
        face_id = str(uuid.uuid4())
        embedding = face.embedding.tolist()
        x1, y1, x2, y2 = face.bbox.astype(int)
        face_img = frame[y1:y2, x1:x2]

        if y2 > y1 and x2 > x1:
            img_path = os.path.join(SAVE_DIR, f"{face_id}.jpg")
            cv2.imwrite(img_path, face_img)

            collection.insert_one({
                "face_id": face_id,
                "embedding": embedding,
                "image_path": img_path,
                "timestamp": datetime.datetime.now()
            })
            print(f"✅ Registered face: {face_id}")

cap.release()
cv2.destroyAllWindows()
