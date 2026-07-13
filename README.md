# 🛡️ AI Image & Video Forensics: Advanced Detection System

An interactive digital forensics application built to detect AI-generated imagery and deepfake video configurations. Utilizing an advanced Vision Transformer (ViT) model coupled with Error Level Analysis (ELA), this tool parses multimedia files to surface pixel inconsistencies, compression anomalies, and artificial noise patterns.

---

## 🚀 Features

### 🖼️ Image Forensics
* **AI Pattern Classification:** Powered by the `Organika/sdxl-detector` model to determine if an image is camera-original or synthetic (`artificial`).
* **Error Level Analysis (ELA):** Generates an on-the-fly digital artifact heatmap. By resaving the image and calculating pixel coordinate disparities, it exposes inconsistencies in compression that flag digital alteration.

### 🎥 Video Forensics (Paranoid Mode)
* **Temporal Frame Scanning:** Decodes target video streams and samples periodic keyframes to spot dynamic deepfake signatures.
* **Suspicion Thresholding:** Evaluates individual frames; if more than 15% of parsed frames trigger high-confidence AI signals, the whole file is flagged.
* **Compression Aware Diagnostics:** Evaluates the impact of aggressive video compression formats (like standard H.264), alerting users when a small file size might yield false negatives due to stripped metadata fingerprints.

---

## ⚙️ Tech Stack & Dependencies

* **Frontend UI:** Streamlit
* **Core Machine Learning:** Hugging Face Transformers (`pipeline`)
* **Computer Vision & Processing:** OpenCV (`cv2`), Pillow (`PIL`)

---

## 🛠️ Installation & Setup

If you want to run this application locally in the future, follow these setup steps:

### 1. Clone the Project
```bash
git clone [https://github.com/Akhil-7770/ai-image-video-detection-system.git](https://github.com/Akhil-7770/ai-image-video-detection-system.git)
cd ai-image-video-detection-system
