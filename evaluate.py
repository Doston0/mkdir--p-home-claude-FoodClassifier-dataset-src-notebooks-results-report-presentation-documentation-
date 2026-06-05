"""
evaluate.py
Model Evaluation — Metrics, Confusion Matrix, Classification Report
Food Image Classification System — CAU Spring 2025-2026

Usage:
    python src/evaluate.py --model_path results/best_model.h5 --dataset dataset/
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, precision_recall_fscore_support
)

from preprocess import get_data_generators, CLASSES


# ─── Argument Parser ─────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate Food Classifier')
    parser.add_argument('--model_path', type=str, default='results/best_model.h5')
    parser.add_argument('--dataset', type=str, default='dataset/')
    parser.add_argument('--save_dir', type=str, default='results/')
    return parser.parse_args()


# ─── Evaluation ──────────────────────────────────────────────────────────────

def evaluate_model(model_path: str, dataset_path: str, save_dir: str):
    """
    Full evaluation pipeline.

    Steps:
        1. Load model and test data
        2. Generate predictions
        3. Compute all metrics
        4. Plot confusion matrix
        5. Print classification report

    Args:
        model_path: Path to saved .h5 model.
        dataset_path: Path to dataset directory.
        save_dir: Where to save output plots.
    """
    os.makedirs(save_dir, exist_ok=True)

    print("Loading model...")
    model = tf.keras.models.load_model(model_path)

    print("Loading test data...")
    _, _, test_gen = get_data_generators(dataset_path)

    # Generate predictions
    print("Generating predictions...")
    y_pred_probs = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = test_gen.classes
    class_names = list(test_gen.class_indices.keys())

    # ── Overall Metrics ───────────────────────────────────────────────────────
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average='weighted'
    )

    print(f"\n{'='*50}")
    print(f" Evaluation Results")
    print(f"{'='*50}")
    print(f" Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f" Precision: {precision:.4f}")
    print(f" Recall:    {recall:.4f}")
    print(f" F1-Score:  {f1:.4f}")
    print(f"{'='*50}\n")

    # ── Per-Class Report ──────────────────────────────────────────────────────
    print("Per-class Classification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))

    # ── Confusion Matrix ──────────────────────────────────────────────────────
    plot_confusion_matrix(y_true, y_pred, class_names, save_dir)

    # ── Top-5 Confidence Analysis ─────────────────────────────────────────────
    plot_confidence_distribution(y_pred_probs, y_true, save_dir)

    return {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1)
    }


# ─── Plot Confusion Matrix ───────────────────────────────────────────────────

def plot_confusion_matrix(y_true: np.ndarray,
                           y_pred: np.ndarray,
                           class_names: list,
                           save_dir: str):
    """
    Plot and save a normalized confusion matrix heatmap.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.
        class_names: List of class name strings.
        save_dir: Save directory.
    """
    cm = confusion_matrix(y_true, y_pred)
    cm_normalized = cm.astype('float') / cm.sum(axis=1, keepdims=True)

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        cm_normalized,
        annot=True,
        fmt='.2f',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
        linewidths=0.5,
        cbar_kws={'shrink': 0.8}
    )

    ax.set_title('Confusion Matrix (Normalized)', fontsize=15, fontweight='bold', pad=15)
    ax.set_ylabel('True Label', fontsize=12)
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)

    plt.tight_layout()
    cm_path = os.path.join(save_dir, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {cm_path}")


# ─── Confidence Distribution ─────────────────────────────────────────────────

def plot_confidence_distribution(y_pred_probs: np.ndarray,
                                  y_true: np.ndarray,
                                  save_dir: str):
    """
    Plot prediction confidence (max probability) for correct vs incorrect predictions.

    Args:
        y_pred_probs: Predicted probability arrays.
        y_true: True label indices.
        save_dir: Save directory.
    """
    y_pred = np.argmax(y_pred_probs, axis=1)
    max_conf = np.max(y_pred_probs, axis=1)
    correct_mask = (y_pred == y_true)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(max_conf[correct_mask], bins=30, alpha=0.6, color='steelblue',
            label='Correct predictions', edgecolor='white')
    ax.hist(max_conf[~correct_mask], bins=30, alpha=0.6, color='tomato',
            label='Incorrect predictions', edgecolor='white')
    ax.set_title('Prediction Confidence Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Confidence (max softmax probability)')
    ax.set_ylabel('Count')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    conf_path = os.path.join(save_dir, 'confidence_distribution.png')
    plt.savefig(conf_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {conf_path}")


# ─── Per-Class Accuracy ───────────────────────────────────────────────────────

def plot_per_class_accuracy(y_true: np.ndarray,
                             y_pred: np.ndarray,
                             class_names: list,
                             save_dir: str):
    """
    Bar chart of per-class accuracy.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.
        class_names: Class name list.
        save_dir: Save directory.
    """
    cm = confusion_matrix(y_true, y_pred)
    per_class_acc = cm.diagonal() / cm.sum(axis=1)

    fig, ax = plt.subplots(figsize=(12, 5))
    colors = ['steelblue' if a >= 0.8 else 'orange' if a >= 0.6 else 'tomato'
              for a in per_class_acc]
    bars = ax.bar(class_names, per_class_acc, color=colors, edgecolor='white')
    ax.axhline(y=np.mean(per_class_acc), color='black', linestyle='--',
               label=f'Mean: {np.mean(per_class_acc):.2f}', linewidth=1.5)
    ax.set_title('Per-Class Accuracy', fontsize=14, fontweight='bold')
    ax.set_ylabel('Accuracy')
    ax.set_ylim(0, 1.1)
    ax.tick_params(axis='x', rotation=45)
    ax.legend()

    for bar, acc in zip(bars, per_class_acc):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f'{acc:.2f}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    save_path = os.path.join(save_dir, 'per_class_accuracy.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")


if __name__ == '__main__':
    args = parse_args()
    metrics = evaluate_model(args.model_path, args.dataset, args.save_dir)
    print("\nFinal Metrics Summary:")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}")
