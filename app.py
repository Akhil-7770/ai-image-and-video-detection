import streamlit as st
from PIL import Image, ImageChops, ImageEnhance
import tempfile
import os
from backend import predict_image, predict_video

# --- ELA Logic ---
def convert_to_ela_image(path, quality):
    original_image = Image.open(path).convert('RGB')
    resaved_name = 'temp_ela.jpg'
    original_image.save(resaved_name, 'JPEG', quality=quality)
    resaved_image = Image.open(resaved_name)
    ela_image = ImageChops.difference(original_image, resaved_image)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0: max_diff = 1
    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    return ela_image

# --- UI Setup ---

# --- SIDEBAR: The "Learning Aspect" ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png")
    st.title("Forensic Lab Control")
    st.markdown("### 🎓 Educational Mode")
    st.info("""
    **How this works:**
    1. **Visual Artifacts:** We use a Vision Transformer (ViT) to look for pixel inconsistencies.
    2. **Compression Analysis:** We check if the video is too compressed (H.264) which hides AI evidence.
    3. **ELA Heatmap:** Error Level Analysis highlights edited regions.
    """)
    st.warning("⚠️ **Limitation:** Highly compressed videos (WhatsApp/Facebook) often strip away the 'AI Fingerprints', leading to False Negatives.")

st.title("🛡️ AI Image & Video Forensics")
st.markdown("### Advanced Detection System")

# TABS
tab1, tab2 = st.tabs(["🖼️ Image Forensics", "🎥 Video Forensics"])

# --- TAB 1: IMAGE ---
with tab1:
    uploaded_file = st.file_uploader("Upload Suspect Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        image = Image.open(uploaded_file)
        
        with col1:
            st.subheader("Suspect Image")
            st.image(image, use_container_width=True)
            
            if st.button('🔍 Run Forensic Analysis'):
                with st.spinner('Analyzing pixel patterns...'):
                    results = predict_image(image)
                    top = results[0]
                    label = top['label']
                    score = top['score'] * 100
                    
                    st.markdown("---")
                    if label == 'artificial':
                        st.error(f"**VERDICT: FAKE (AI Generated)**")
                        st.metric("Confidence", f"{score:.1f}%")
                        st.write("Reason: Unnatural pixel noise patterns detected.")
                    else:
                        st.success(f"**VERDICT: REAL (Likely Camera)**")
                        st.metric("Confidence", f"{score:.1f}%")
                        st.write("Reason: Consistent sensor noise and natural lighting physics.")

        with col2:
            st.subheader("Technical Artifacts (ELA)")
            st.caption("Brighter areas indicate potential manipulation or high error levels.")
            with open("temp_upload.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())
            ela = convert_to_ela_image("temp_upload.jpg", 90)
            st.image(ela, use_container_width=True)

# --- TAB 2: VIDEO ---
with tab2:
    st.info("ℹ️ Video analysis checks frames for temporal artifacts.")
    uploaded_video = st.file_uploader("Upload Suspect Video", type=["mp4", "mov"])
    
    if uploaded_video is not None:
        # Save temp file
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_video.read())
        
        # --- LEARNING ASPECT: Check File Size/Compression ---
        file_size_mb = os.path.getsize(tfile.name) / (1024 * 1024)
        st.video(tfile.name)
        
        st.markdown(f"**File Analysis:** `{file_size_mb:.2f} MB`")
        
        if file_size_mb < 5.0:
            st.warning("⚠️ **High Compression Detected:** This file is very small. Compression artifacts may hide AI evidence.")

        if st.button('🎥 Scan Video Frames'):
            with st.spinner('Extracting and analyzing keyframes...'):
                result = predict_video(tfile.name)
                
                label = result['label']
                score = result['score'] * 100
                
                st.markdown("---")
                if label == 'artificial':
                    st.error(f"## 🚨 DEEPFAKE DETECTED")
                    st.metric("Fake Frame Ratio", f"{score:.1f}%")
                else:
                    st.success(f"## ✅ LIKELY REAL")
                    st.metric("Confidence", f"{score:.1f}%")
                    
                    # EDUCATIONAL EXPLANATION FOR "WRONG" ANSWERS
                    with st.expander("Why does it say 'Real' if I know it's Fake?"):
                        st.markdown("""
                        **The 'CSI Effect' Explanation:**
                        * **Compression:** Video compression (like H.264 used in MP4) acts like a 'blur' filter. It smooths out the tiny, invisible pixel noise that AI models leave behind.
                        * **The Result:** To the AI, a highly compressed Deepfake looks just like a highly compressed Real video. The 'evidence' was deleted by the compressor.
                        """)