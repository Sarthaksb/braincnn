import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import DenseNet201
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Suppress excessive TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def parse_args():
    parser = argparse.ArgumentParser(description="Train DenseNet201 for Brain Tumor Classification")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size for training")
    parser.add_argument("--steps-per-epoch", type=int, default=None, help="Steps per epoch (None for full dataset)")
    parser.add_argument("--val-steps", type=int, default=None, help="Validation steps per epoch (None for full)")
    parser.add_argument("--img-size", type=int, default=224, help="Input image dimension (224x224)")
    parser.add_argument("--data-dir", type=str, default="", help="Path to brain tumor classification dataset")
    parser.add_argument("--save-dir", type=str, default="models", help="Directory to save model checkpoints")
    return parser.parse_args()

def find_dataset_dir(custom_path=""):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    
    candidates = [
        os.path.abspath("Brain-Tumar-classificaltion-using-CNN-main/input/brain-tumor-classification-mri"),
        os.path.abspath("input/brain-tumor-classification-mri"),
        os.path.abspath("../input/brain-tumor-classification-mri"),
        r"c:\Users\aditi\Downloads\brain-tumor-dataset-sartaj",
        r"c:\Users\aditi\Downloads\brain_tumor_mri_dataset\Dataset",
    ]
    for c in candidates:
        if os.path.exists(os.path.join(c, "Training")) and os.path.exists(os.path.join(c, "Testing")):
            return c
    raise FileNotFoundError("Could not locate brain tumor dataset directory. Specify with --data-dir")

def build_model(num_classes=4, input_shape=(224, 224, 3)):
    print(f"Loading pre-trained DenseNet201 with ImageNet weights...")
    densenet = DenseNet201(
        include_top=False,
        weights="imagenet",
        input_shape=input_shape
    )
    for layer in densenet.layers:
        layer.trainable = False

    top = densenet.output
    top = Flatten(name="flatten")(top)
    top = Dense(256, activation="relu")(top)
    top = Dropout(0.3)(top)
    top = Dense(num_classes, activation="softmax")(top)

    model = Model(inputs=densenet.input, outputs=top)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=RMSprop(learning_rate=0.00001),
        metrics=["accuracy"]
    )
    return model

def main():
    args = parse_args()
    data_dir = find_dataset_dir(args.data_dir)
    print(f"Dataset root: {data_dir}")

    train_dir = os.path.join(data_dir, "Training")
    test_dir = os.path.join(data_dir, "Testing")

    os.makedirs(args.save_dir, exist_ok=True)
    os.makedirs("working", exist_ok=True)

    print("Setting up data generators...")
    train_gen = ImageDataGenerator(
        rescale=1.0 / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    test_gen = ImageDataGenerator(rescale=1.0 / 255)

    train_data = train_gen.flow_from_directory(
        directory=train_dir,
        target_size=(args.img_size, args.img_size),
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=True
    )

    val_data = test_gen.flow_from_directory(
        directory=test_dir,
        target_size=(args.img_size, args.img_size),
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=False
    )

    print(f"Classes detected: {train_data.class_indices}")
    num_classes = len(train_data.class_indices)

    model = build_model(num_classes=num_classes, input_shape=(args.img_size, args.img_size, 3))

    best_model_path = os.path.join(args.save_dir, "densenet101.h5")
    callbacks = [
        ModelCheckpoint(best_model_path, monitor="val_loss", mode="min", save_best_only=True, verbose=1),
        EarlyStopping(monitor="val_loss", min_delta=0, patience=3, verbose=1, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=5, verbose=1, min_delta=0.000001)
    ]

    nb_train_samples = train_data.samples
    nb_val_samples = val_data.samples

    steps_per_epoch = args.steps_per_epoch if args.steps_per_epoch else max(1, nb_train_samples // args.batch_size)
    validation_steps = args.val_steps if args.val_steps else max(1, nb_val_samples // args.batch_size)

    print(f"\nStarting training for {args.epochs} epochs ({steps_per_epoch} steps/epoch, {validation_steps} val_steps/epoch)...")
    history = model.fit(
        train_data,
        steps_per_epoch=steps_per_epoch,
        epochs=args.epochs,
        callbacks=callbacks,
        validation_data=val_data,
        validation_steps=validation_steps
    )

    # Save to working directory as well
    working_model_path = os.path.join("working", "densenet101.h5")
    model.save(working_model_path)
    print(f"Saved model to: {working_model_path} and {best_model_path}")

    # Evaluate
    print("\nEvaluating model on validation data...")
    val_loss, val_acc = model.evaluate(val_data)
    print(f"Final Validation Loss: {val_loss:.4f}, Accuracy: {val_acc*100:.2f}%")

    # Save training curves plot
    epochs_range = range(1, len(history.history['loss']) + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(epochs_range, history.history['loss'], label='Train Loss', marker='o')
    ax1.plot(epochs_range, history.history['val_loss'], label='Val Loss', marker='o')
    ax1.set_title('Loss (Lower Means Better)')
    ax1.set_xlabel('Epochs')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2.plot(epochs_range, history.history['accuracy'], label='Train Accuracy', marker='o')
    ax2.plot(epochs_range, history.history['val_accuracy'], label='Val Accuracy', marker='o')
    ax2.set_title('Accuracy (Higher Means Better)')
    ax2.set_xlabel('Epochs')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    curve_path = "training_curves.png"
    plt.savefig(curve_path, dpi=150)
    print(f"Saved training curves to {curve_path}")

if __name__ == "__main__":
    main()
