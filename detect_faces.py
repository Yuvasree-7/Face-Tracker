
# import cv2
# from ultralytics import YOLO
# from face_matcher import match_and_label

# model = YOLO("models/yolov8n.pt")

# def detect_in_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS) or 25
#     frame_idx = 0
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame_idx += 1
#         results = model(frame, conf=0.25)
#         for r in results:
#             for box in r.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 face_crop = frame[y1:y2, x1:x2]
#                 name = match_and_label(face_crop)
#                 if name:
#                     sec = frame_idx / fps
#                     print(f"[{sec:.2f}s] Detected: {name}")
#         cv2.imshow("Detect", frame)
#         if cv2.waitKey(1) == 27:
#             break
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     detect_in_video("uploads/your_video.mp4")



import cv2
from ultralytics import YOLO
from face_matcher import match_and_label

model = YOLO("models/yolov8n.pt")  # You can use yolov8m or yolov8l for better accuracy

def detect_in_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        results = model(frame, conf=0.25)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                face_crop = frame[y1:y2, x1:x2]
                name = match_and_label(face_crop)

                if name:
                    sec = frame_idx / fps
                    print(f"[{sec:.2f}s] Detected: {name}")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, name[:8], (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.imshow("YOLO + InsightFace", frame)
        if cv2.waitKey(1) == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_in_video("uploads/sample.mp4")  # Replace with actual path
