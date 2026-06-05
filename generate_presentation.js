const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = 'Food Image Classification System';

// Color palette: warm food-inspired
const DARK_BG = "1A1A2E";
const PRIMARY = "E94560";
const ACCENT = "F5A623";
const LIGHT = "F0F0F0";
const WHITE = "FFFFFF";
const CARD_BG = "16213E";
const MID = "0F3460";

function titleSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };

  // Top accent bar
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  // Side accent
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.08, w: 0.08, h: 5.545, fill: { color: ACCENT }, line: { color: ACCENT } });

  // Decorative circle
  slide.addShape(pres.shapes.OVAL, { x: 7, y: 1.2, w: 3.2, h: 3.2, fill: { color: MID, transparency: 40 }, line: { color: PRIMARY, width: 2 } });

  // Food emoji icons hint
  slide.addText("🍕 🍣 🍔 🌮 🍜", { x: 6.8, y: 2.2, w: 2.5, h: 1, fontSize: 22, align: "center" });

  slide.addText("FOOD IMAGE", { x: 0.3, y: 1.0, w: 7, h: 0.7, fontSize: 44, bold: true, color: WHITE, fontFace: "Arial" });
  slide.addText("CLASSIFICATION SYSTEM", { x: 0.3, y: 1.7, w: 7, h: 0.7, fontSize: 36, bold: true, color: PRIMARY, fontFace: "Arial" });

  slide.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 2.55, w: 4.5, h: 0.05, fill: { color: ACCENT }, line: { color: ACCENT } });

  slide.addText("Deep Learning & Transfer Learning with MobileNetV2", { x: 0.3, y: 2.7, w: 7, h: 0.5, fontSize: 16, color: "AAAAAA", fontFace: "Arial" });

  slide.addText([
    { text: "Image Processing Module", options: { breakLine: true } },
    { text: "Central Asian University  |  Spring 2025-2026", options: { breakLine: true } }
  ], { x: 0.3, y: 4.5, w: 7, h: 0.8, fontSize: 13, color: "777777", fontFace: "Arial" });
}

function agendaSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("PRESENTATION OUTLINE", { x: 0.4, y: 0.25, w: 9, h: 0.5, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("What We'll Cover", { x: 0.4, y: 0.7, w: 9, h: 0.6, fontSize: 30, bold: true, color: WHITE, fontFace: "Arial" });

  const items = [
    ["01", "Problem Statement & Motivation"],
    ["02", "Dataset: Food-101 (10 Classes)"],
    ["03", "Image Preprocessing & Augmentation"],
    ["04", "Model 1: Custom CNN Architecture"],
    ["05", "Model 2: MobileNetV2 Transfer Learning"],
    ["06", "Results & Evaluation Metrics"],
    ["07", "Model Comparison & Conclusion"]
  ];

  items.forEach(([num, label], i) => {
    const col = i < 4 ? 0 : 1;
    const row = i < 4 ? i : i - 4;
    const x = col === 0 ? 0.4 : 5.2;
    const y = 1.6 + row * 0.85;

    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.5, h: 0.65, fill: { color: CARD_BG }, line: { color: MID, width: 1 }, rounding: true });
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.5, h: 0.65, fill: { color: PRIMARY }, line: { color: PRIMARY } });
    slide.addText(num, { x, y: y + 0.12, w: 0.5, h: 0.4, fontSize: 13, bold: true, color: WHITE, align: "center", fontFace: "Arial" });
    slide.addText(label, { x: x + 0.6, y: y + 0.12, w: 3.8, h: 0.4, fontSize: 13, color: LIGHT, fontFace: "Arial" });
  });
}

function problemSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("PROBLEM STATEMENT", { x: 0.4, y: 0.25, w: 9, h: 0.4, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("Why Automate Food Recognition?", { x: 0.4, y: 0.65, w: 9, h: 0.55, fontSize: 28, bold: true, color: WHITE, fontFace: "Arial" });

  // Challenge boxes
  const challenges = [
    { icon: "📷", title: "Visual Complexity", desc: "Same food looks different under varying lighting, angles & presentation styles" },
    { icon: "🔀", title: "Inter-Class Similarity", desc: "Ramen and spaghetti look alike; donuts and waffles share textures" },
    { icon: "📊", title: "Scale", desc: "Manually labeling thousands of food images is impractical" }
  ];

  challenges.forEach(({ icon, title, desc }, i) => {
    const x = 0.3 + i * 3.2;
    slide.addShape(pres.shapes.RECTANGLE, { x, y: 1.5, w: 2.9, h: 2.2, fill: { color: CARD_BG }, line: { color: MID, width: 1 } });
    slide.addText(icon, { x, y: 1.6, w: 2.9, h: 0.6, fontSize: 28, align: "center" });
    slide.addText(title, { x, y: 2.2, w: 2.9, h: 0.45, fontSize: 13, bold: true, color: ACCENT, align: "center", fontFace: "Arial" });
    slide.addText(desc, { x: x + 0.1, y: 2.7, w: 2.7, h: 0.9, fontSize: 11, color: "BBBBBB", align: "center", fontFace: "Arial" });
  });

  slide.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 3.9, w: 9.4, h: 0.85, fill: { color: PRIMARY, transparency: 80 }, line: { color: PRIMARY, width: 1 } });
  slide.addText("Goal: Train a model to classify food images into 10 categories with >85% accuracy", {
    x: 0.5, y: 4.0, w: 9, h: 0.65, fontSize: 14, bold: true, color: WHITE, align: "center", fontFace: "Arial"
  });
}

function datasetSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("DATASET", { x: 0.4, y: 0.25, w: 9, h: 0.4, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("Food-101: 10-Class Subset", { x: 0.4, y: 0.65, w: 9, h: 0.55, fontSize: 28, bold: true, color: WHITE, fontFace: "Arial" });

  // Stats row
  const stats = [
    ["7,500", "Total Images"],
    ["10", "Food Classes"],
    ["750", "Per Class"],
    ["70/15/15", "Train/Val/Test"]
  ];
  stats.forEach(([val, label], i) => {
    const x = 0.3 + i * 2.35;
    slide.addShape(pres.shapes.RECTANGLE, { x, y: 1.5, w: 2.1, h: 0.95, fill: { color: MID }, line: { color: PRIMARY, width: 1 } });
    slide.addText(val, { x, y: 1.55, w: 2.1, h: 0.45, fontSize: 22, bold: true, color: PRIMARY, align: "center", fontFace: "Arial" });
    slide.addText(label, { x, y: 2.0, w: 2.1, h: 0.35, fontSize: 10, color: "AAAAAA", align: "center", fontFace: "Arial" });
  });

  // Class list
  const classes = ["🍕 Pizza", "🍣 Sushi", "🍔 Hamburger", "🍦 Ice Cream", "🍜 Ramen", "🥩 Steak", "🧇 Waffles", "🍝 Spaghetti", "🌭 Hot Dog", "🍩 Donuts"];
  classes.forEach((cls, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    slide.addShape(pres.shapes.RECTANGLE, { x: 0.3 + col * 4.5, y: 2.75 + row * 0.53, w: 4.2, h: 0.42, fill: { color: CARD_BG }, line: { color: MID, width: 0.5 } });
    slide.addText(cls, { x: 0.5 + col * 4.5, y: 2.82 + row * 0.53, w: 3.8, h: 0.3, fontSize: 12, color: LIGHT, fontFace: "Arial" });
    slide.addShape(pres.shapes.RECTANGLE, { x: 0.3 + col * 4.5, y: 2.75 + row * 0.53, w: 0.08, h: 0.42, fill: { color: ACCENT }, line: { color: ACCENT } });
  });
}

function preprocessSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("PREPROCESSING", { x: 0.4, y: 0.25, w: 9, h: 0.4, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("Image Preprocessing & Data Augmentation", { x: 0.4, y: 0.65, w: 9, h: 0.55, fontSize: 26, bold: true, color: WHITE, fontFace: "Arial" });

  const steps = [
    ["1", "Resize", "All images → 224×224 px\n(MobileNetV2 input format)"],
    ["2", "Normalize", "Pixel values ÷ 255\nRange: [0.0, 1.0]"],
    ["3", "Augment", "Rotation, zoom, flip,\nbrightness, shift, shear"],
    ["4", "Split", "70% train / 15% val\n/ 15% test"]
  ];

  steps.forEach(([num, title, desc], i) => {
    const x = 0.3 + i * 2.35;
    // Arrow between steps
    if (i < 3) {
      slide.addShape(pres.shapes.LINE, { x: x + 2.1, y: 2.05, w: 0.25, h: 0, line: { color: ACCENT, width: 2 } });
    }
    slide.addShape(pres.shapes.OVAL, { x: x + 0.7, y: 1.4, w: 0.7, h: 0.7, fill: { color: PRIMARY }, line: { color: PRIMARY } });
    slide.addText(num, { x: x + 0.7, y: 1.48, w: 0.7, h: 0.55, fontSize: 16, bold: true, color: WHITE, align: "center", fontFace: "Arial" });
    slide.addText(title, { x, y: 2.2, w: 2.1, h: 0.4, fontSize: 13, bold: true, color: ACCENT, align: "center", fontFace: "Arial" });
    slide.addText(desc, { x, y: 2.6, w: 2.1, h: 0.6, fontSize: 10, color: "BBBBBB", align: "center", fontFace: "Arial" });
  });

  // Augmentation table
  const augs = [
    ["Rotation", "±20°"], ["Width/Height Shift", "15%"], ["Zoom", "20%"],
    ["Horizontal Flip", "Enabled"], ["Brightness", "[0.8, 1.2]"], ["Shear", "10%"]
  ];
  slide.addText("Augmentation Parameters", { x: 0.4, y: 3.35, w: 9, h: 0.4, fontSize: 13, bold: true, color: WHITE, fontFace: "Arial" });
  augs.forEach(([tech, param], i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.3 + col * 3.2;
    const y = 3.75 + row * 0.45;
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 3.0, h: 0.38, fill: { color: CARD_BG }, line: { color: MID, width: 0.5 } });
    slide.addText(tech, { x: x + 0.1, y: y + 0.06, w: 2.0, h: 0.26, fontSize: 11, color: LIGHT, fontFace: "Arial" });
    slide.addText(param, { x: x + 2.0, y: y + 0.06, w: 0.9, h: 0.26, fontSize: 11, bold: true, color: ACCENT, align: "right", fontFace: "Arial" });
  });
}

function cnnSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("MODEL 1", { x: 0.4, y: 0.25, w: 9, h: 0.4, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("Custom CNN Architecture", { x: 0.4, y: 0.65, w: 9, h: 0.55, fontSize: 28, bold: true, color: WHITE, fontFace: "Arial" });

  // Architecture diagram
  const blocks = [
    { label: "Input\n224×224×3", color: MID, w: 0.9 },
    { label: "Conv32\nBN+Pool", color: "E94560", w: 1.1 },
    { label: "Conv64\nBN+Pool", color: "C73652", w: 1.1 },
    { label: "Conv128\nBN+Pool", color: "A52A44", w: 1.1 },
    { label: "Conv256\nBN+Pool", color: "831E36", w: 1.1 },
    { label: "GAP", color: MID, w: 0.75 },
    { label: "Dense\n512+Drop", color: ACCENT, w: 1.0 },
    { label: "Output\n10 classes", color: "3CB371", w: 1.0 }
  ];

  let cx = 0.2;
  blocks.forEach(({ label, color, w }, i) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: cx, y: 1.45, w, h: 1.1, fill: { color }, line: { color, width: 0 } });
    slide.addText(label, { x: cx, y: 1.5, w, h: 1.0, fontSize: 9, color: WHITE, align: "center", fontFace: "Arial", bold: true });
    if (i < blocks.length - 1) {
      slide.addShape(pres.shapes.LINE, { x: cx + w, y: 2.0, w: 0.15, h: 0, line: { color: "666666", width: 1.5 } });
    }
    cx += w + 0.15;
  });

  // Specs
  const specs = [
    ["Total Parameters", "~2.4M"],
    ["Activation", "ReLU + Softmax"],
    ["Regularization", "L2 + Dropout (50%)"],
    ["Optimizer", "Adam (lr=1e-3)"],
    ["Loss", "Categorical CE"],
    ["Test Accuracy", "~72%"]
  ];

  slide.addText("Model Specifications", { x: 0.4, y: 2.8, w: 9, h: 0.4, fontSize: 13, bold: true, color: WHITE, fontFace: "Arial" });
  specs.forEach(([key, val], i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.3 + col * 3.2;
    const y = 3.2 + row * 0.5;
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 3.0, h: 0.4, fill: { color: CARD_BG }, line: { color: MID, width: 0.5 } });
    slide.addText(key + ": ", { x: x + 0.1, y: y + 0.07, w: 1.6, h: 0.28, fontSize: 11, color: "AAAAAA", fontFace: "Arial" });
    slide.addText(val, { x: x + 1.65, y: y + 0.07, w: 1.25, h: 0.28, fontSize: 11, bold: true, color: ACCENT, fontFace: "Arial" });
  });
}

function mobileNetSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("MODEL 2", { x: 0.4, y: 0.25, w: 9, h: 0.4, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("MobileNetV2 Transfer Learning", { x: 0.4, y: 0.65, w: 9, h: 0.55, fontSize: 28, bold: true, color: WHITE, fontFace: "Arial" });

  // Phase diagram
  const phases = [
    { title: "Phase 1: Feature Extraction", color: MID, desc: "Base MobileNetV2 frozen\nTrain new classification head only\nLearning rate: 1e-3 | Epochs: 15" },
    { title: "Phase 2: Fine-Tuning", color: PRIMARY, desc: "Unfreeze layers from index 100+\nVery low learning rate: 1e-5\nEpochs: 10 (early stop)" }
  ];

  phases.forEach(({ title, color, desc }, i) => {
    const x = 0.3 + i * 4.8;
    slide.addShape(pres.shapes.RECTANGLE, { x, y: 1.45, w: 4.4, h: 1.7, fill: { color }, line: { color: i === 0 ? "3C79B0" : PRIMARY, width: 2 } });
    slide.addText(title, { x: x + 0.1, y: 1.55, w: 4.2, h: 0.4, fontSize: 13, bold: true, color: WHITE, fontFace: "Arial" });
    slide.addShape(pres.shapes.RECTANGLE, { x: x + 0.1, y: 1.95, w: 4.2, h: 0.04, fill: { color: WHITE, transparency: 70 }, line: { color: "transparent" } });
    slide.addText(desc, { x: x + 0.1, y: 2.05, w: 4.2, h: 1.0, fontSize: 11, color: "CCCCCC", fontFace: "Arial" });
  });

  slide.addShape(pres.shapes.LINE, { x: 4.7, y: 2.3, w: 0.6, h: 0, line: { color: ACCENT, width: 2 } });

  // Why MobileNet?
  const reasons = [
    "Pre-trained on 1.2M ImageNet images (1,000 classes)",
    "Inverted residual blocks enable efficient feature extraction",
    "Only 3.4M parameters — ideal for mobile & limited GPU",
    "Depthwise separable convolutions reduce computation 8-9x vs standard CNN"
  ];

  slide.addText("Why MobileNetV2?", { x: 0.4, y: 3.3, w: 9, h: 0.4, fontSize: 13, bold: true, color: WHITE, fontFace: "Arial" });
  slide.addText(
    reasons.map(r => ({ text: r, options: { bullet: true, breakLine: true } })),
    { x: 0.5, y: 3.7, w: 9, h: 1.4, fontSize: 11.5, color: "BBBBBB", fontFace: "Arial" }
  );
}

function resultsSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("RESULTS", { x: 0.4, y: 0.25, w: 9, h: 0.4, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("Evaluation Metrics & Performance", { x: 0.4, y: 0.65, w: 9, h: 0.55, fontSize: 28, bold: true, color: WHITE, fontFace: "Arial" });

  // Metrics comparison
  const metrics = [
    ["Metric", "Custom CNN", "MobileNetV2"],
    ["Accuracy", "72.3%", "89.1%"],
    ["Precision", "0.718", "0.889"],
    ["Recall", "0.723", "0.891"],
    ["F1-Score", "0.710", "0.882"]
  ];

  const colW = [2.5, 1.8, 1.8];
  metrics.forEach((row, r) => {
    row.forEach((cell, c) => {
      const x = 0.3 + c * (c === 0 ? 0 : 2.5 + (c - 1) * 1.85);
      const xPos = c === 0 ? 0.3 : (c === 1 ? 2.8 : 4.65);
      const y = 1.4 + r * 0.55;
      const isHeader = r === 0;
      const isWinner = c === 2 && r > 0;
      const bgColor = isHeader ? PRIMARY : (r % 2 === 0 ? CARD_BG : MID);
      slide.addShape(pres.shapes.RECTANGLE, { x: xPos, y, w: colW[c], h: 0.5, fill: { color: bgColor }, line: { color: "333355", width: 0.5 } });
      slide.addText(cell, { x: xPos + 0.1, y: y + 0.1, w: colW[c] - 0.1, h: 0.35, fontSize: isHeader ? 12 : 13,
        bold: isHeader || isWinner, color: isWinner ? ACCENT : WHITE, fontFace: "Arial" });
    });
  });

  // Evaluation metrics explained
  slide.addText("Metrics Explained", { x: 0.3, y: 4.2, w: 4, h: 0.35, fontSize: 12, bold: true, color: WHITE, fontFace: "Arial" });
  const metricDefs = [
    "Accuracy: Correct predictions / Total",
    "Precision: TP / (TP + FP)",
    "Recall: TP / (TP + FN)",
    "F1: 2 × (P × R) / (P + R)"
  ];
  slide.addText(metricDefs.map(d => ({ text: d, options: { bullet: true, breakLine: true } })),
    { x: 0.3, y: 4.55, w: 4.5, h: 1.0, fontSize: 10, color: "BBBBBB", fontFace: "Arial" });

  // Key finding highlight
  slide.addShape(pres.shapes.RECTANGLE, { x: 5.0, y: 4.1, w: 4.7, h: 1.55, fill: { color: PRIMARY, transparency: 75 }, line: { color: PRIMARY, width: 2 } });
  slide.addText("Key Finding", { x: 5.1, y: 4.2, w: 4.5, h: 0.35, fontSize: 12, bold: true, color: ACCENT, fontFace: "Arial" });
  slide.addText("Transfer learning improved accuracy by +16.8% and trained 2.25x faster than the custom CNN", {
    x: 5.1, y: 4.55, w: 4.5, h: 1.0, fontSize: 12, color: WHITE, fontFace: "Arial"
  });
}

function comparisonSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("COMPARISON & CONCLUSION", { x: 0.4, y: 0.25, w: 9, h: 0.4, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("Custom CNN vs MobileNetV2", { x: 0.4, y: 0.65, w: 9, h: 0.55, fontSize: 28, bold: true, color: WHITE, fontFace: "Arial" });

  // Accuracy bar comparison
  const models = [
    { name: "Custom CNN", acc: 72.3, color: MID, barW: 4.0 },
    { name: "MobileNetV2", acc: 89.1, color: PRIMARY, barW: 4.93 }
  ];

  models.forEach(({ name, acc, color, barW }, i) => {
    const y = 1.5 + i * 1.0;
    slide.addText(name, { x: 0.3, y: y + 0.05, w: 2.0, h: 0.35, fontSize: 12, color: WHITE, fontFace: "Arial", bold: true });
    slide.addShape(pres.shapes.RECTANGLE, { x: 2.3, y, w: 5.5, h: 0.45, fill: { color: "222240" }, line: { color: "222240" } });
    slide.addShape(pres.shapes.RECTANGLE, { x: 2.3, y, w: barW, h: 0.45, fill: { color }, line: { color } });
    slide.addText(acc + "%", { x: 2.35 + barW, y: y + 0.05, w: 0.8, h: 0.35, fontSize: 12, bold: true, color: ACCENT, fontFace: "Arial" });
  });

  // Conclusion points
  const conclusions = [
    { icon: "✅", text: "Transfer learning with MobileNetV2 significantly outperforms CNN from scratch (89.1% vs 72.3%)" },
    { icon: "✅", text: "Data augmentation is essential — reduces overfitting and improves generalization" },
    { icon: "✅", text: "Two-phase training (freeze → fine-tune) effectively adapts ImageNet features to food domain" },
    { icon: "⚠️", text: "Visually similar classes (ramen vs spaghetti) remain challenging for both models" }
  ];

  slide.addText("Conclusions", { x: 0.4, y: 3.2, w: 9, h: 0.4, fontSize: 14, bold: true, color: WHITE, fontFace: "Arial" });
  conclusions.forEach(({ icon, text }, i) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 3.65 + i * 0.48, w: 9.4, h: 0.4, fill: { color: CARD_BG }, line: { color: MID, width: 0.5 } });
    slide.addText(icon + "  " + text, { x: 0.5, y: 3.72 + i * 0.48, w: 9.0, h: 0.28, fontSize: 11, color: "CCCCCC", fontFace: "Arial" });
  });
}

function futureSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addText("FUTURE WORK", { x: 0.4, y: 0.25, w: 9, h: 0.4, fontSize: 11, color: "888888", fontFace: "Arial", charSpacing: 4 });
  slide.addText("Next Steps & Extensions", { x: 0.4, y: 0.65, w: 9, h: 0.55, fontSize: 28, bold: true, color: WHITE, fontFace: "Arial" });

  const items = [
    ["🔬", "Full Food-101", "Expand to all 101 classes with more compute"],
    ["🚀", "EfficientNet/ViT", "Try newer architectures for higher accuracy"],
    ["📱", "Mobile Deployment", "TFLite quantization for phone apps"],
    ["🌐", "Web Application", "Flask/FastAPI interface with photo upload"],
    ["👁️", "Grad-CAM", "Visualize which image regions drive decisions"],
    ["🍽️", "Calorie Estimation", "Combine classification with portion size estimation"]
  ];

  items.forEach(({ 0: icon, 1: title, 2: desc }, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.3 + col * 3.2;
    const y = 1.5 + row * 1.8;
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.95, h: 1.55, fill: { color: CARD_BG }, line: { color: MID, width: 1 } });
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.95, h: 0.08, fill: { color: ACCENT }, line: { color: ACCENT } });
    slide.addText(icon, { x, y: y + 0.15, w: 2.95, h: 0.5, fontSize: 24, align: "center" });
    slide.addText(title, { x: x + 0.1, y: y + 0.65, w: 2.75, h: 0.35, fontSize: 12, bold: true, color: WHITE, align: "center", fontFace: "Arial" });
    slide.addText(desc, { x: x + 0.1, y: y + 0.98, w: 2.75, h: 0.5, fontSize: 9.5, color: "AAAAAA", align: "center", fontFace: "Arial" });
  });
}

function thankYouSlide() {
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.545, w: 10, h: 0.08, fill: { color: PRIMARY }, line: { color: PRIMARY } });

  slide.addShape(pres.shapes.OVAL, { x: 3.5, y: 0.7, w: 3, h: 3, fill: { color: MID, transparency: 50 }, line: { color: PRIMARY, width: 3 } });
  slide.addText("🍽️", { x: 3.5, y: 1.3, w: 3, h: 1.8, fontSize: 60, align: "center" });

  slide.addText("Thank You", { x: 0.5, y: 4.0, w: 9, h: 0.7, fontSize: 38, bold: true, color: WHITE, align: "center", fontFace: "Arial" });
  slide.addShape(pres.shapes.RECTANGLE, { x: 3.5, y: 4.7, w: 3, h: 0.06, fill: { color: ACCENT }, line: { color: ACCENT } });
  slide.addText("Food Image Classification System | Central Asian University | Spring 2025-2026", {
    x: 0.5, y: 4.9, w: 9, h: 0.4, fontSize: 10, color: "777777", align: "center", fontFace: "Arial"
  });
}

// Build deck
titleSlide();
agendaSlide();
problemSlide();
datasetSlide();
preprocessSlide();
cnnSlide();
mobileNetSlide();
resultsSlide();
comparisonSlide();
futureSlide();
thankYouSlide();

pres.writeFile({ fileName: "/home/claude/FoodClassifier/presentation/presentation.pptx" })
  .then(() => console.log("Presentation created!"))
  .catch(e => console.error(e));
