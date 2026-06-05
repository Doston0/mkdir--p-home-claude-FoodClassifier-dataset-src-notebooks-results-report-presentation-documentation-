"""
preprocess.py
Image Preprocessing and Augmentation Pipeline
Food Image Classification System — CAU Spring 2025-2026
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

# ─── Constants ──────────────────────────────────────────────────────────────
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
CLASSES = [
    'pizza', 'sushi', 'hamburger', 'ice_cream', 'ramen',
    'steak', 'waffles', 'spaghetti_bolognese', 'hot_dog', 'donuts'
]
NUM_CLASSES = len(CLASSES)


# ─── Data Generators ────────────────────────────────────────────────────────

def get_data_generators(dataset_path: str):
    """
    Create train, validation, and test data generators with augmentation.

    Args:
        dataset_path: Path to dataset directory structured as class subfolders.

    Returns:
        train_gen, val_gen, test_gen
    """
    # Training augmentation
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,           # Normalize pixel values to [0, 1]
        rotation_range=20,             # Random rotation ±20 degrees
        width_shift_range=0.15,        # Horizontal shift
        height_shift_range=0.15,       # Vertical shift
        shear_range=0.1,               # Shear transformation
        zoom_range=0.2,                # Random zoom
        horizontal_flip=True,          # Mirror images
        brightness_range=[0.8, 1.2],   # Random brightness
        fill_mode='nearest',           # Fill strategy after transformation
        validation_split=0.15          # 15% for validation
    )

    # Validation / test — only rescale, no augmentation
    val_test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    train_gen = train_datagen.flow_from_directory(
        os.path.join(dataset_path, 'train'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )

    val_gen = val_test_datagen.flow_from_directory(
        os.path.join(dataset_path, 'val'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    test_gen = val_test_datagen.flow_from_directory(
        os.path.join(dataset_path, 'test'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    return train_gen, val_gen, test_gen


# ─── Single Image Preprocessing ─────────────────────────────────────────────

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load, resize, and normalize a single image for inference.

    Args:
        image_path: Path to the image file.

    Returns:
        Preprocessed image array of shape (1, 224, 224, 3).
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV loads as BGR
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)            # Add batch dimension
    return img


# ─── Exploratory Data Analysis ───────────────────────────────────────────────

def plot_class_distribution(dataset_path: str, save_path: str = None):
    """
    Plot the number of images per class.

    Args:
        dataset_path: Path to the 'train' subdirectory.
        save_path: If provided, save the figure to this path.
    """
    class_counts = {}
    train_path = os.path.join(dataset_path, 'train')

    for cls in sorted(os.listdir(train_path)):
        cls_path = os.path.join(train_path, cls)
        if os.path.isdir(cls_path):
            class_counts[cls] = len(os.listdir(cls_path))

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(class_counts.keys(), class_counts.values(), color='steelblue', edgecolor='white')
    ax.set_title('Class Distribution — Training Set', fontsize=14, fontweight='bold')
    ax.set_xlabel('Food Category', fontsize=12)
    ax.set_ylabel('Number of Images', fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    for bar, count in zip(bars, class_counts.values()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                str(count), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    plt.show()


def plot_sample_images(dataset_path: str, save_path: str = None):
    """
    Display one sample image per class in a grid.

    Args:
        dataset_path: Path to the dataset.
        save_path: Optional save path for the figure.
    """
    train_path = os.path.join(dataset_path, 'train')
    classes = sorted(os.listdir(train_path))

    fig, axes = plt.subplots(2, 5, figsize=(15, 7))
    axes = axes.flatten()

    for i, cls in enumerate(classes[:10]):
        cls_path = os.path.join(train_path, cls)
        img_file = os.listdir(cls_path)[0]
        img = cv2.imread(os.path.join(cls_path, img_file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (150, 150))
        axes[i].imshow(img)
        axes[i].set_title(cls.replace('_', ' ').title(), fontsize=10)
        axes[i].axis('off')

    plt.suptitle('Sample Images per Class', fontsize=14, fontweight='bold')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    plt.show()


# ─── Augmentation Demo ───────────────────────────────────────────────────────

def show_augmented_samples(image_path: str, save_path: str = None):
    """
    Show the effect of augmentation on a single image.

    Args:
        image_path: Path to a sample image.
        save_path: Optional save path.
    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    img_batch = np.expand_dims(img, 0)

    datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True,
        brightness_range=[0.6, 1.4]
    )

    aug_gen = datagen.flow(img_batch, batch_size=1)
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    axes = axes.flatten()
    axes[0].imshow(img.astype('uint8'))
    axes[0].set_title('Original', fontweight='bold')
    axes[0].axis('off')

    for i in range(1, 10):
        aug_img = next(aug_gen)[0].astype('uint8')
        axes[i].imshow(aug_img)
        axes[i].set_title(f'Augmented {i}')
        axes[i].axis('off')

    plt.suptitle('Data Augmentation Examples', fontsize=14, fontweight='bold')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    print("Preprocessing module loaded.")
    print(f"Image size: {IMG_SIZE}")
    print(f"Classes ({NUM_CLASSES}): {', '.join(CLASSES)}")
