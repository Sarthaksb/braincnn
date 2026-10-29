import os
import glob
import numpy as np
from PIL import Image
import streamlit as st
import tensorflow as tf

st.set_page_config(
    page_title="Brain Tumor Classification | DenseNet201",
    page_icon="🧠",
    layout="wide"
)

CLASS_NAMES = [
    "Glioma Tumor",
    "Meningioma Tumor",
    "No Tumor",
    "Pituitary Tumor"
]

CLASS_INFO = {
    "Glioma Tumor": "A common type of tumor originating in the glial cells of the brain or spinal cord. Gliomas can be low-grade or high-grade (such as glioblastomas).",
    "Meningioma Tumor": "A tumor that arises from the meninges — the membranes that surround the brain and spinal cord. Most are benign and slow-growing.",
    "No Tumor": "The MRI scan displays normal brain tissue anatomy without detectable signs of tumor lesions.",
    "Pituitary Tumor": "An abnormal growth in the pituitary gland at the base of the brain. Most pituitary tumors are benign adenomas affecting hormone regulation."
}

CLASS_COLORS = {
    "Glioma Tumor": "#E63946",
    "Meningioma Tumor": "#F4A261",
    "No Tumor": "#2A9D8F",
    "Pituitary Tumor": "#457B9D"
}

@st.cache_resource(show_spinner="Loading deep learning model weights...")
def load_classification_model():
    model_paths = [
        "models/densenet101.h5",
        "working/densenet101.h5",
        "Brain-Tumar-classificaltion-using-CNN-main/working/densenet101.h5",
        r"C:\Trained Models\densenet101.h5"
    ]
    for p in model_paths:
        if os.path.exists(p):
            try:
                model = tf.keras.models.load_model(p, compile=False)
                # Warm-up graph for instantaneous inference
                _ = model(np.zeros((1, 224, 224, 3), dtype=np.float32), training=False)
                return model, p
            except Exception as e:
                pass
    return None, None

def predict_mri(model, pil_image):
    resized = pil_image.convert("RGB").resize((224, 224))
    x = np.array(resized, dtype=np.float32) / 255.0
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x, verbose=0)[0]
    pred_idx = int(np.argmax(preds))
    return CLASS_NAMES[pred_idx], float(preds[pred_idx]) * 100.0, preds

# --- Header ---
st.title("🧠 Brain Tumor Classification using CNN")
st.markdown(
    "Detect and classify brain tumors from **Magnetic Resonance Imaging (MRI)** scans "
    "using transfer learning with **DenseNet201**."
)

model, model_path = load_classification_model()

# --- Sidebar ---
st.sidebar.header("⚙️ System Status")
if model:
    st.sidebar.success(f"Model Loaded\n\n`{os.path.basename(model_path)}`")
else:
    st.sidebar.warning("⚠️ Model weights not found. Please train the model first or select a path.")

st.sidebar.markdown("---")
st.sidebar.header("🧪 Sample MRI Scans")

# Find sample test images
sample_dirs = [
    r"c:\Users\aditi\Downloads\brain-tumor-dataset-sartaj\Testing",
    os.path.abspath("input/brain-tumor-classification-mri/Testing"),
    os.path.abspath("Brain-Tumar-classificaltion-using-CNN-main/input/brain-tumor-classification-mri/Testing"),
]

sample_images = {}
for sdir in sample_dirs:
    if os.path.exists(sdir):
        for cname in ["glioma_tumor", "meningioma_tumor", "no_tumor", "pituitary_tumor"]:
            folder = os.path.join(sdir, cname)
            if os.path.exists(folder):
                files = glob.glob(os.path.join(folder, "*.*"))
                if files:
                    clean_name = cname.replace("_", " ").title()
                    sample_images[clean_name] = files[0]
        if sample_images:
            break

selected_sample = None
if sample_images:
    sample_choice = st.sidebar.selectbox("Choose a sample MRI:", ["None"] + list(sample_images.keys()))
    if sample_choice != "None":
        selected_sample = sample_images[sample_choice]

# --- Main Layout ---
col1, col2 = st.columns([1, 1], gap="large")

image_to_process = None

with col1:
    st.subheader("📥 Input MRI Scan")
    uploaded_file = st.file_uploader("Upload Brain MRI scan (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image_to_process = Image.open(uploaded_file)
        st.image(image_to_process, caption="Uploaded MRI Scan", use_container_width=True)
    elif selected_sample:
        image_to_process = Image.open(selected_sample)
        st.image(image_to_process, caption=f"Sample: {os.path.basename(selected_sample)}", use_container_width=True)
    else:
        st.info("Please upload an MRI image or pick a sample scan from the sidebar to analyze.")

with col2:
    st.subheader("🔬 Diagnostic Analysis")
    if image_to_process is not None:
        if model is None:
            st.error("No model available to perform inference. Run `python train.py` first.")
        else:
            with st.spinner("Analyzing MRI scan..."):
                pred_class, confidence, probabilities = predict_mri(model, image_to_process)

            color = CLASS_COLORS.get(pred_class, "#333333")
            st.markdown(
                f"""
                <div style="background-color: {color}22; border-left: 6px solid {color}; padding: 16px; border-radius: 6px; margin-bottom: 20px;">
                    <h3 style="margin: 0; color: {color};">Diagnosis: {pred_class}</h3>
                    <p style="margin: 5px 0 0 0; font-size: 1.15rem; font-weight: 600;">Confidence: {confidence:.2f}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(CLASS_INFO.get(pred_class, ""))

            st.markdown("#### Probability Distribution")
            for idx, cname in enumerate(CLASS_NAMES):
                prob = float(probabilities[idx])
                pct = prob * 100
                st.write(f"**{cname}**: `{pct:5.2f}%`")
                st.progress(min(1.0, prob))
    else:
        st.write("Awaiting MRI scan input...")

