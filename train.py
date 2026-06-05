"""
train.py
Model Training Script
Food Image Classification System — CAU Spring 2025-2026

Usage:
    python src/train.py --dataset dataset/ --model mobilenet --epochs 20
    python src/train.py --dataset dataset/ --model cnn --epochs 30
"""

import os
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from preprocess import get_data_generators
from model import (build_custom_cnn, build_mobilenet,
                   unfreeze_for_fine_tuning, get_callbacks)


# ─── Argument Parser ─────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description='Train Food Classifier')
    parser.add_argument('--dataset', type=str, default='dataset/',
                        help='Path to dataset directory')
    parser.add_argument('--model', type=str, default='mobilenet',
                        choices=['mobilenet', 'cnn'],
                        help='Model architecture to use')
    parser.add_argument('--epochs', type=int, default=20,
                        help='Number of training epochs')
    parser.add_argument('--fine_tune_epochs', type=int, default=10,
                        help='Additional epochs for fine-tuning (MobileNet only)')
    parser.add_argument('--save_dir', type=str, default='results/',
                        help='Directory to save results')
    return parser.parse_args()


# ─── Training ────────────────────────────────────────────────────────────────

def train(args):
    os.makedirs(args.save_dir, exist_ok=True)

    print(f"\n{'='*50}")
    print(f" Food Image Classifier — Training")
    print(f" Model: {args.model.upper()}")
    print(f" Epochs: {args.epochs}")
    print(f"{'='*50}\n")

    # 1. Load data
    print("Loading data generators...")
    train_gen, val_gen, test_gen = get_data_generators(args.dataset)
    print(f"Train batches: {len(train_gen)}")
    print(f"Val batches:   {len(val_gen)}")
    print(f"Test batches:  {len(test_gen)}\n")

    # 2. Build model
    model_path = os.path.join(args.save_dir, 'best_model.h5')

    if args.model == 'mobilenet':
        model, base_model = build_mobilenet()
        print("Phase 1: Feature extraction (base frozen)")
        history_phase1 = model.fit(
            train_gen,
            epochs=args.epochs,
            validation_data=val_gen,
            callbacks=get_callbacks(model_path),
            verbose=1
        )

        # Fine-tuning phase
        print("\nPhase 2: Fine-tuning (unfreeze top layers)")
        unfreeze_for_fine_tuning(model, base_model, fine_tune_at=100)
        history_phase2 = model.fit(
            train_gen,
            epochs=args.fine_tune_epochs,
            validation_data=val_gen,
            callbacks=get_callbacks(model_path, patience=3),
            verbose=1
        )

        # Merge histories
        history = merge_histories(history_phase1, history_phase2)

    else:
        model = build_custom_cnn()
        result = model.fit(
            train_gen,
            epochs=args.epochs,
            validation_data=val_gen,
            callbacks=get_callbacks(model_path),
            verbose=1
        )
        history = result.history

    # 3. Save history
    history_path = os.path.join(args.save_dir, 'training_history.json')
    with open(history_path, 'w') as f:
        # Convert numpy floats to Python floats for JSON serialization
        history_serializable = {k: [float(v) for v in vals]
                                 for k, vals in history.items()}
        json.dump(history_serializable, f, indent=2)
    print(f"\nHistory saved: {history_path}")

    # 4. Plot training curves
    plot_training_curves(history, args.save_dir)

    # 5. Evaluate on test set
    print("\nEvaluating on test set...")
    model.load_weights(model_path)
    test_loss, test_acc = model.evaluate(test_gen, verbose=0)
    print(f"Test Accuracy: {test_acc:.4f} ({test_acc * 100:.2f}%)")
    print(f"Test Loss:     {test_loss:.4f}")

    # Save summary
    summary_path = os.path.join(args.save_dir, 'training_summary.json')
    with open(summary_path, 'w') as f:
        json.dump({
            'model': args.model,
            'epochs_run': args.epochs,
            'test_accuracy': float(test_acc),
            'test_loss': float(test_loss),
            'best_val_accuracy': float(max(history.get('val_accuracy', [0])))
        }, f, indent=2)

    print(f"\nTraining complete. Model saved to: {model_path}")
    return model, history


# ─── Utilities ───────────────────────────────────────────────────────────────

def merge_histories(h1, h2):
    """Merge two Keras history objects into one dict."""
    h1_dict = h1.history
    h2_dict = h2.history
    merged = {}
    for key in h1_dict:
        merged[key] = h1_dict[key] + h2_dict.get(key, [])
    return merged


def plot_training_curves(history: dict, save_dir: str):
    """
    Plot and save accuracy and loss curves.

    Args:
        history: Dictionary with keys 'accuracy', 'val_accuracy', 'loss', 'val_loss'.
        save_dir: Directory to save the plots.
    """
    epochs = range(1, len(history['accuracy']) + 1)

    # Accuracy plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(epochs, history['accuracy'], 'b-o', label='Train Accuracy', markersize=4)
    ax.plot(epochs, history['val_accuracy'], 'r-o', label='Val Accuracy', markersize=4)
    ax.set_title('Training vs Validation Accuracy', fontsize=14, fontweight='bold')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy')
    ax.legend()
    ax.grid(True, alpha=0.3)
    acc_path = os.path.join(save_dir, 'accuracy_curve.png')
    plt.tight_layout()
    plt.savefig(acc_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {acc_path}")

    # Loss plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(epochs, history['loss'], 'b-o', label='Train Loss', markersize=4)
    ax.plot(epochs, history['val_loss'], 'r-o', label='Val Loss', markersize=4)
    ax.set_title('Training vs Validation Loss', fontsize=14, fontweight='bold')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.legend()
    ax.grid(True, alpha=0.3)
    loss_path = os.path.join(save_dir, 'loss_curve.png')
    plt.tight_layout()
    plt.savefig(loss_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {loss_path}")


if __name__ == '__main__':
    args = parse_args()
    train(args)
