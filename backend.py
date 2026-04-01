# backend.py
from transformers import pipeline
from PIL import Image
import cv2  

# 1. Load the Pipeline (Organika model)
def load_detector():
    if 'pipe' not in globals():
        global pipe
        print("Loading model... (Organika/SDXL)")
        pipe = pipeline("image-classification", model="Organika/sdxl-detector")
    return pipe

# 2. Predict Image
def predict_image(image_object):
    detector = load_detector()
    results = detector(image_object)
    return results

# 3. Predict Video (Paranoid Mode for Forensic Lab)
def predict_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    skip_frames = 15  
    
    fake_frame_count = 0
    total_checked = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % skip_frames == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Predict
            result = predict_image(pil_image)
            
            # Check if THIS specific frame is AI
            is_fake_frame = False
            for r in result:
                if r['label'] == 'artificial' and r['score'] > 0.70:
                    is_fake_frame = True
                    break
            
            if is_fake_frame:
                fake_frame_count += 1
                
            total_checked += 1
            
        frame_count += 1
        
    cap.release()
    
    if total_checked == 0:
        return {"label": "Error", "score": 0.0}
    
    fake_ratio = fake_frame_count / total_checked
    
    if fake_ratio > 0.15:  # Threshold: 15% suspicious frames = FAKE
        return {"label": "artificial", "score": fake_ratio}
    else:
        return {"label": "human", "score": 1 - fake_ratio}