"""
model.py
Model Architecture Definitions
Food Image Classification System — CAU Spring 2025-2026

Two models:
  1. Custom CNN (built from scratch)
  2. Transfer Learning with MobileNetV2 (recommended)
"""

import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)

IMG_SIZE = (224, 224, 3)
NUM_CLASSES = 10


# ─── Model 1: Custom CNN ─────────────────────────────────────────────────────

def build_custom_cnn(num_classes: int = NUM_CLASSES) -> tf.keras.Model:
    """
    Build a custom CNN from scratch.

    Architecture:
        Conv2D(32) → MaxPool → Conv2D(64) → MaxPool →
        Conv2D(128) → MaxPool → Conv2D(256) → MaxPool →
        GlobalAveragePooling → Dense(512) → Dropout → Output

    Args:
        num_classes: Number of output classes.

    Returns:
        Compiled Keras model.
    """
    model = models.Sequential(name='Custom_CNN')

    # Block 1
    model.add(layers.Conv2D(32, (3, 3), activation='relu',
                            padding='same', input_shape=IMG_SIZE))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # Block 2
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # Block 3
    model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # Block 4
    model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same',
                            kernel_regularizer=regularizers.l2(1e-4)))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # Classifier head
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dense(512, activation='relu',
                           kernel_regularizer=regularizers.l2(1e-4)))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(num_classes, activation='softmax'))

    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


# ─── Model 2: Transfer Learning — MobileNetV2 ───────────────────────────────

def build_mobilenet(num_classes: int = NUM_CLASSES,
                    fine_tune_at: int = 100) -> tf.keras.Model:
    """
    Build a MobileNetV2-based model with fine-tuning.

    Strategy:
        1. Freeze all layers, train the new head (feature extraction).
        2. Unfreeze layers after `fine_tune_at`, continue training at low LR.

    Args:
        num_classes: Number of output classes.
        fine_tune_at: Layer index from which to unfreeze for fine-tuning.

    Returns:
        Compiled Keras model.
    """
    base_model = MobileNetV2(
        input_shape=IMG_SIZE,
        include_top=False,         # Remove the ImageNet classification head
        weights='imagenet'         # Pre-trained weights
    )
    base_model.trainable = False   # Freeze base initially

    # New classification head
    inputs = tf.keras.Input(shape=IMG_SIZE)
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = tf.keras.Model(inputs, outputs, name='MobileNetV2_FoodClassifier')

    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model, base_model


def unfreeze_for_fine_tuning(model: tf.keras.Model,
                              base_model,
                              fine_tune_at: int = 100,
                              learning_rate: float = 1e-5):
    """
    Unfreeze top layers of the base model for fine-tuning.

    Args:
        model: Full compiled model.
        base_model: The base MobileNetV2 model reference.
        fine_tune_at: Index from which layers become trainable.
        learning_rate: Lower LR for fine-tuning (avoid destroying pre-trained weights).
    """
    base_model.trainable = True

    # Freeze layers before fine_tune_at
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print(f"Fine-tuning from layer {fine_tune_at} onwards.")
    print(f"Trainable layers: {sum(1 for l in base_model.layers if l.trainable)}")


# ─── Callbacks ───────────────────────────────────────────────────────────────

def get_callbacks(model_save_path: str = 'results/best_model.h5',
                  patience: int = 5):
    """
    Standard training callbacks.

    Args:
        model_save_path: Where to save the best model checkpoint.
        patience: Epochs to wait before early stopping.

    Returns:
        List of Keras callbacks.
    """
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=patience,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            filepath=model_save_path,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]
    return callbacks


# ─── Model Summary Utility ───────────────────────────────────────────────────

def print_model_info(model: tf.keras.Model):
    """Print model summary and parameter count."""
    model.summary()
    total = model.count_params()
    trainable = sum(tf.keras.backend.count_params(w)
                    for w in model.trainable_weights)
    print(f"\nTotal parameters:     {total:,}")
    print(f"Trainable parameters: {trainable:,}")
    print(f"Non-trainable:        {total - trainable:,}")


if __name__ == '__main__':
    print("=== Custom CNN ===")
    cnn = build_custom_cnn()
    print_model_info(cnn)

    print("\n=== MobileNetV2 ===")
    mobilenet, base = build_mobilenet()
    print_model_info(mobilenet)
