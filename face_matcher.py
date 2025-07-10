
# from insightface.app import FaceAnalysis
# from pymongo import MongoClient
# from scipy.spatial.distance import cosine
# import numpy as np
# from urllib.parse import quote_plus

# username = quote_plus("22ad062")
# password = quote_plus("Student@123")
# mongo_uri = f"mongodb+srv://{username}:{password}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"
# client = MongoClient(mongo_uri)
# db = client["face_tracker"]
# collection = db["registered_faces"]

# model = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
# model.prepare(ctx_id=0)

# def get_registered_faces():
#     return [{"id": doc["face_id"], "embed": np.array(doc["embedding"])} for doc in collection.find()]

# def match_and_label(face_crop):
#     faces = model.get(face_crop)
#     if not faces:
#         return None

#     reg_faces = get_registered_faces()
#     face_emb = faces[0].embedding
#     best_match = None
#     best_score = 1

#     for person in reg_faces:
#         dist = cosine(face_emb, person["embed"])
#         if dist < best_score:
#             best_score = dist
#             best_match = person["id"]

#     return best_match if best_score < 0.5 else None



from insightface.app import FaceAnalysis
from pymongo import MongoClient
from scipy.spatial.distance import cosine
import numpy as np
from urllib.parse import quote_plus

# MongoDB config
username = quote_plus("22ad062")
password = quote_plus("Student@123")
mongo_uri = f"mongodb+srv://{username}:{password}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"
client = MongoClient(mongo_uri)
db = client["face_tracker"]
collection = db["registered_faces"]

# InsightFace
model = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
model.prepare(ctx_id=0)

def get_registered_faces():
    return [{"id": doc["face_id"], "embed": np.array(doc["embedding"])} for doc in collection.find()]

def match_and_label(face_crop):
    faces = model.get(face_crop)
    if not faces:
        return None

    reg_faces = get_registered_faces()
    face_emb = faces[0].embedding
    best_match = None
    best_score = 1.0

    for person in reg_faces:
        dist = cosine(face_emb, person["embed"])
        if dist < best_score:
            best_score = dist
            best_match = person["id"]

    return best_match if best_score < 0.45 else None
