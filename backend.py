# backend.py
from transformers import pipeline
from PIL import Image
import cv2

MODEL_NAME = "Organika/sdxl-detector"
_pipe = None


# 1. Load the pipeline once and reuse it
def load_detector():
    global _pipe
    if _pipe is None:
        print(f"Loading model... ({MODEL_NAME})")
        _pipe = pipeline("image-classification", model=MODEL_NAME)
    return _pipe


# 2. Predict image
def predict_image(image_object):
    detector = load_detector()
    return detector(image_object.convert("RGB"))


# 3. Predict video (Paranoid Mode for Forensic Lab)
def predict_video(video_path, skip_frames=15, frame_threshold=0.70, video_threshold=0.15):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fake_frame_count = 0
    total_checked = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % skip_frames == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = predict_image(Image.fromarray(rgb_frame))

            # Is THIS frame confidently AI-generated?
            if any(r['label'] == 'artificial' and r['score'] > frame_threshold for r in result):
                fake_frame_count += 1
            total_checked += 1

        frame_count += 1

    cap.release()

    if total_checked == 0:
        return {"label": "Error", "score": 0.0}

    fake_ratio = fake_frame_count / total_checked

    # More than 15% suspicious frames = flag the whole video
    if fake_ratio > video_threshold:
        return {"label": "artificial", "score": fake_ratio}
    return {"label": "human", "score": 1 - fake_ratio}
