from pymongo import MongoClient
from urllib.parse import quote_plus

# === Replace with your actual password ===
raw_password = "Student@123"  # replace this

# === Safely encode the password ===
encoded_password = quote_plus(raw_password)

# === Construct the MongoDB URI ===
MONGO_URI = f"mongodb+srv://22ad062:{encoded_password}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"

# === MongoDB Database & Collection ===
DB_NAME = "facerecognition"
COLLECTION_NAME = "registered_faces"

# === Connect and Test ===
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    print("✅ Connected to MongoDB Atlas\n")
    print("🧠 Registered Faces in Database:")

    for doc in collection.find():
        print("Face ID:", doc.get("face_id"))
        print("Timestamp:", doc.get("timestamp"))
        print("Image Path:", doc.get("image_path"))
        print("-" * 40)

except Exception as e:
    print("❌ MongoDB Connection Error:", e)
