import json
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

# === MongoDB Config ===
username = quote_plus("22ad062")
password = quote_plus("Student@123")
mongo_uri = f"mongodb+srv://{username}:{password}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"

client = MongoClient(mongo_uri)
db = client["face_tracker"]
logs_col = db["tracking_logs"]

# === Prepare JSON Log ===
entries = logs_col.find().sort("timestamp", 1)
log_data = []

for entry in entries:
    log_data.append({
        "track_id": entry.get("track_id"),
        "source": entry.get("source"),
        "source_name": entry.get("source_name"),
        "timestamp": entry.get("timestamp").strftime("%Y-%m-%d %H:%M:%S"),
        "bbox": entry.get("bbox")
    })

# === Save to JSON ===
with open("face_tracking_logs.json", "w") as f:
    json.dump(log_data, f, indent=4)

print("✅ Exported face tracking logs to face_tracking_logs.json")
