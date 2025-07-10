# from pymongo import MongoClient
# import urllib.parse
# import certifi

# # Replace with your actual credentials
# username = urllib.parse.quote_plus("22ad062")
# password = urllib.parse.quote_plus("Student@123")  # encode special characters like @

# # Your actual cluster and database info
# uri = f"mongodb+srv://{username}:{password}@facerecognition.zcyfrxm.mongodb.net/?retryWrites=true&w=majority&tls=true"

# # Connect with SSL verification
# client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)

# try:
#     client.admin.command("ping")
#     print("✅ Connected to MongoDB Atlas")
# except Exception as e:
#     print("❌ MongoDB Atlas connection failed:", e)


import os

model_dir = os.path.expanduser("~/.insightface/models/antelopev2")
required_files = [
    "det_10g.onnx",
    "1k3d68.onnx",
    "2d106det.onnx",
    "w600k_r50.onnx",
    "genderage.onnx"
]

missing = [f for f in required_files if not os.path.exists(os.path.join(model_dir, f))]

if missing:
    print("❌ Missing files:")
    for f in missing:
        print(f"- {f}")
else:
    print("✅ All required model files are present.")
