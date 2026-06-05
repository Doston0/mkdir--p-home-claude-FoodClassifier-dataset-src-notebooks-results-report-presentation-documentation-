"""
predict.py
Single Image Inference
Food Image Classification System — CAU Spring 2025-2026

Usage:
    python src/predict.py --image path/to/food.jpg --model_path results/best_model.h5
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2

from preprocess import preprocess_image, CLASSES

# ─── Argument Parser ─────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description='Food Image Prediction')
    parser.add_argument('--image', type=str, required=True,
                        help='Path to the input food image')
    parser.add_argument('--model_path', type=str, default='results/best_model.h5',
                        help='Path to the trained model')
    parser.add_argument('--top_k', type=int, default=3,
                        help='Show top-K predictions')
    return parser.parse_args()


# ─── Prediction ───────────────────────────────────────────────────────────────

def predict(image_path: str,
            model_path: str,
            top_k: int = 3,
            visualize: bool = True) -> dict:
    """
    Predict food category from a single image.

    Args:
        image_path: Path to input image.
        model_path: Path to trained .h5 model.
        top_k: Number of top predictions to return.
        visualize: If True, display prediction chart.

    Returns:
        Dictionary with top-K predictions and confidence scores.
    """
    # Load model
    model = tf.keras.models.load_model(model_path)

    # Preprocess image
    img_array = preprocess_image(image_path)

    # Predict
    probs = model.predict(img_array, verbose=0)[0]
    top_k_indices = np.argsort(probs)[::-1][:top_k]

    results = {
        'predictions': [
            {
                'rank': i + 1,
                'class': CLASSES[idx],
                'confidence': float(probs[idx]),
                'percentage': f"{probs[idx] * 100:.1f}%"
            }
            for i, idx in enumerate(top_k_indices)
        ],
        'top_prediction': CLASSES[top_k_indices[0]],
        'top_confidence': float(probs[top_k_indices[0]])
    }

    # Print results
    print(f"\n{'='*40}")
    print(f" Prediction Results")
    print(f"{'='*40}")
    for pred in results['predictions']:
        bar = '█' * int(pred['confidence'] * 30)
        print(f"  {pred['rank']}. {pred['class']:<25} {pred['percentage']:>6}  {bar}")
    print(f"{'='*40}")
    print(f" Top prediction: {results['top_prediction'].upper()}")
    print(f" Confidence:     {results['top_confidence']*100:.1f}%")
    print(f"{'='*40}\n")

    if visualize:
        visualize_prediction(image_path, results['predictions'])

    return results


# ─── Visualization ───────────────────────────────────────────────────────────

def visualize_prediction(image_path: str, predictions: list):
    """
    Display the input image alongside a bar chart of top predictions.

    Args:
        image_path: Path to input image.
        predictions: List of prediction dicts from predict().
    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: image
    axes[0].imshow(img)
    axes[0].set_title('Input Image', fontsize=13, fontweight='bold')
    axes[0].axis('off')

    # Right: prediction bar chart
    classes = [p['class'].replace('_', ' ').title() for p in predictions]
    confidences = [p['confidence'] for p in predictions]
    colors = ['steelblue' if i > 0 else 'tomato' for i in range(len(predictions))]

    bars = axes[1].barh(classes[::-1], confidences[::-1],
                        color=colors[::-1], edgecolor='white')
    axes[1].set_title('Top Predictions', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Confidence')
    axes[1].set_xlim(0, 1)

    for bar, conf in zip(bars, confidences[::-1]):
        axes[1].text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                     f'{conf * 100:.1f}%', va='center', fontsize=10)

    plt.suptitle(
        f"Predicted: {predictions[0]['class'].replace('_', ' ').title()} "
        f"({predictions[0]['percentage']})",
        fontsize=14, fontweight='bold', color='darkred'
    )
    plt.tight_layout()
    plt.savefig('results/prediction_output.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Saved: results/prediction_output.png")


if __name__ == '__main__':
    args = parse_args()
    predict(args.image, args.model_path, args.top_k)
