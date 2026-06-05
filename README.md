# Food Image Classification System

A deep learning-based food recognition system that classifies images into 10 food categories using Convolutional Neural Networks (CNN) and Transfer Learning with MobileNetV2.

## Project Overview

This project implements an end-to-end image classification pipeline for food recognition. It covers:
- Image preprocessing and augmentation
- Custom CNN architecture
- Transfer learning with MobileNetV2
- Evaluation with accuracy, precision, recall, F1-score, and confusion matrix

## Dataset

**Food-101 (subset — 10 classes)**  
Source: [https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/)

Classes used: pizza, sushi, hamburger, ice_cream, ramen, steak, waffles, spaghetti_bolognese, hot_dog, donuts

- Total images: ~7,500 (750 per class)
- Train/Val/Test split: 70% / 15% / 15%

## Repository Structure

```
FoodClassifier/
├── README.md
├── requirements.txt
├── dataset/              # Raw and processed data (not tracked by git)
├── src/
│   ├── preprocess.py     # Image preprocessing and augmentation
│   ├── model.py          # CNN and MobileNetV2 model definitions
│   ├── train.py          # Training script
│   ├── evaluate.py       # Evaluation and metrics
│   └── predict.py        # Single-image inference
├── notebooks/
│   └── FoodClassifier.ipynb  # Main Jupyter notebook (full pipeline)
├── results/
│   ├── accuracy_curve.png
│   ├── loss_curve.png
│   └── confusion_matrix.png
├── report/
│   └── technical_report.pdf
├── presentation/
│   └── presentation.pdf
└── documentation/
    └── internship_report.pdf
```

## Setup & Installation

```bash
git clone https://github.com/YOUR_USERNAME/FoodClassifier.git
cd FoodClassifier
pip install -r requirements.txt
```

## Usage

### Run the full pipeline (Jupyter Notebook)
```bash
jupyter notebook notebooks/FoodClassifier.ipynb
```

### Train the model
```bash
python src/train.py --epochs 20 --model mobilenet
```

### Evaluate
```bash
python src/evaluate.py --model_path results/best_model.h5
```

### Predict a single image
```bash
python src/predict.py --image path/to/food.jpg
```

## Results

| Model         | Test Accuracy | F1-Score |
|---------------|--------------|----------|
| Custom CNN    | ~72%         | ~0.71    |
| MobileNetV2   | ~89%         | ~0.88    |

## Tech Stack

- Python 3.10
- TensorFlow / Keras
- OpenCV
- NumPy, Pandas, Matplotlib, Seaborn
- scikit-learn

## Author

Central Asian University — Image Processing Module  
Spring 2025–2026 Resit Examination
