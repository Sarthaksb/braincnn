# 🧠 Brain Tumor Classification using CNN (DenseNet201)

An automated deep learning system for detecting and classifying brain tumors from **Magnetic Resonance Imaging (MRI)** scans into four distinct categories:
- **Glioma Tumor**
- **Meningioma Tumor**
- **Pituitary Tumor**
- **No Tumor (Healthy Control)**

---

## 📌 Project Overview
Brain tumors are among the most aggressive neurological conditions requiring rapid and accurate diagnosis. Manual interpretation of hundreds of MRI scan slices is time-consuming and subject to inter-observer variability. 

This project implements an end-to-end computer-aided diagnosis (CAD) pipeline leveraging **Transfer Learning** with the **DenseNet201** architecture. DenseNet’s dense connectivity pattern eliminates the vanishing gradient problem and ensures strong feature reuse across convolutional layers.

---

## 📊 Dataset Details
* **Dataset:** Brain Tumor Classification (MRI) Benchmark
* **Source:** Sartaj Bhuvaji et al. ([Kaggle Dataset](https://www.kaggle.com/datasets/sartajbhuvaji/brain-tumor-classification-mri))
* **Total Scans:** 3,264 MRI images
  * **Training Set:** 2,870 images (Glioma: 826, Meningioma: 822, Pituitary: 827, No Tumor: 395)
  * **Testing Set:** 394 images (Glioma: 100, Meningioma: 115, Pituitary: 74, No Tumor: 105)

---

## 🛠️ Technology Stack
* **Language:** Python 3.11
* **Deep Learning:** TensorFlow 2.x, Keras 3.x
* **Backbone Model:** DenseNet201 (Pre-trained on ImageNet)
* **Web UI:** Streamlit
* **Image Processing:** Pillow (PIL), Keras Preprocessing
* **Scientific Computing:** NumPy, SciPy
* **Visualization:** Matplotlib

---

## 🚀 How to Run

### 1. Launch the Interactive Web Application
Double-click `run_app.bat` or run:
```bash
python -m streamlit run app.py
```
*Open http://localhost:8501 in your browser to upload MRI scans and view real-time classifications with confidence scores.*

### 2. Predict on Single MRI Scan (CLI)
```bash
python predict.py --image "path/to/mri_scan.jpg"
```

### 3. Train or Fine-tune the Model
Double-click `run_training.bat` or run:
```bash
python train.py --epochs 20 --batch-size 64
```

### 4. Jupyter Notebook
Open `Brain-Tumar-classificaltion-using-CNN-main/Code/brain-tumor-classification-with-custom-cnn.ipynb` in VS Code or JupyterLab.

---

## 📁 Repository Structure
```text
├── app.py                                       # Streamlit web dashboard
├── train.py                                     # End-to-end model training script
├── predict.py                                   # Command-line single-image inference
├── run_app.bat                                  # 1-click launcher for Web UI
├── run_training.bat                             # 1-click launcher for Training
├── training_curves.png                          # Training loss & accuracy curves
├── Brain_Tumor_Presentation_and_Viva_Guide.docx # Complete presentation & viva guide (Word)
├── Presentation_and_Viva_Guide.txt              # Plain text presentation guide
├── Brain_Tumor_Project_Presentation_Guide.pdf   # Presentation guide (PDF)
├── Brain-Tumar-classificaltion-using-CNN-main/
│   ├── Code/
│   │   └── brain-tumor-classification-with-custom-cnn.ipynb
│   └── Documentation's/
└── .gitignore
```

