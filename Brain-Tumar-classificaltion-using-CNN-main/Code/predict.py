import os
import sys
import argparse
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Suppress excessive TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CLASS_NAMES = [
    "Glioma Tumor",
    "Meningioma Tumor",
    "No Tumor",
    "Pituitary Tumor"
]

def find_model_path(custom_path=""):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    
    candidates = [
        "models/densenet101.h5",
        "working/densenet101.h5",
        "Brain-Tumar-classificaltion-using-CNN-main/working/densenet101.h5",
        r"C:\Trained Models\densenet101.h5",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def predict_single_image(model, img_path, target_size=(224, 224)):
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image not found: {img_path}")
        
    img = image.load_img(img_path, target_size=target_size)
    x = image.img_to_array(img)
    x = x / 255.0
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x, verbose=0)[0]
    pred_idx = np.argmax(preds)
    pred_class = CLASS_NAMES[pred_idx]
    confidence = float(preds[pred_idx]) * 100.0

    return pred_class, confidence, preds

def main():
    parser = argparse.ArgumentParser(description="Predict brain tumor type from MRI scan")
    parser.add_argument("--image", type=str, required=True, help="Path to input MRI image (.jpg, .png)")
    parser.add_argument("--model", type=str, default="", help="Path to trained model (.h5)")
    args = parser.parse_args()

    model_path = find_model_path(args.model)
    if not model_path:
        print("Error: Trained model not found! Please train the model first using: python train.py")
        sys.exit(1)

    print(f"Loading model: {model_path}...")
    model = tf.keras.models.load_model(model_path, compile=False)

    pred_class, confidence, probabilities = predict_single_image(model, args.image)

    print("\n" + "=" * 50)
    print(f"MRI Image: {args.image}")
    print(f"Predicted Diagnosis: {pred_class.upper()}")
    print(f"Confidence:          {confidence:.2f}%")
    print("=" * 50)
    print("Class Probabilities:")
    for idx, cname in enumerate(CLASS_NAMES):
        bar = "#" * int(probabilities[idx] * 25)
        print(f"  {cname:<18}: {probabilities[idx]*100:6.2f}% | {bar}")
    print("=" * 50)

if __name__ == "__main__":
    main()
