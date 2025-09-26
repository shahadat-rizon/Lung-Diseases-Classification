# Lung-Diseases-Classification

A comprehensive machine learning and deep learning project for classifying lung diseases from X-ray images using various approaches including transfer learning with InceptionV3, SVM, Random Forest, and XGBoost.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- VS Code (recommended)
- Git

### Setup for VS Code Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shahadat-rizon/Lung-Diseases-Classification.git
   cd Lung-Diseases-Classification
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install development dependencies** (optional):
   ```bash
   pip install -r dev-requirements.txt
   ```

6. **Open in VS Code**:
   ```bash
   code .
   ```

### VS Code Extensions
When you open the project in VS Code, it will recommend installing the following extensions:
- Python
- Jupyter
- Jupyter Keymap
- Jupyter Notebook Renderers
- Pylint
- Black Formatter

## 📊 Dataset

**Lung X-Ray Image Dataset**:

The "Lung X-Ray Image Dataset" is a comprehensive collection of X-ray images that plays a pivotal role in the detection and diagnosis of lung diseases. This dataset contains a large number of high-quality X-ray images, meticulously collected from diverse sources, including hospitals, clinics, and healthcare institutions.

### Dataset Contents:

- **Total Number of Images**: 3,475 X-ray images
- **Classes within the Dataset**:
  - **Normal (1250 Images)**: Healthy lung conditions.
  - **Lung Opacity (1125 Images)**: Varying degrees of lung abnormalities.
  - **Viral Pneumonia (1100 Images)**: Cases of viral pneumonia.

📁 [Download the dataset](https://data.mendeley.com/datasets/9d55cttn5h/1)

This resource supports the detection, classification, and understanding of lung diseases — perfect for building prediction models and performing advanced analysis.

## 🛠️ Usage

### Using the Python Module
```python
from lung_diseases_classification import LungDiseaseClassifier

# Initialize classifier
classifier = LungDiseaseClassifier(data_path="path/to/your/dataset")

# Setup data generators
classifier.setup_data_generators()

# Build and train InceptionV3 model
classifier.build_inception_model()
classifier.train_inception_model()

# Plot training history
classifier.plot_training_history()
```

### Using the Jupyter Notebook
Open `Lung Diseases Classification.ipynb` in VS Code or Jupyter Lab to run the interactive analysis.

## 📁 Project Structure

```
Lung-Diseases-Classification/
├── .vscode/                    # VS Code configuration
│   ├── settings.json          # Python and Jupyter settings
│   ├── extensions.json        # Recommended extensions
│   └── launch.json           # Debug configurations
├── Lung Diseases Classification.ipynb  # Main Jupyter notebook
├── lung_diseases_classification.py     # Python module version
├── requirements.txt           # Production dependencies
├── dev-requirements.txt       # Development dependencies
├── pyproject.toml            # Modern Python project configuration
├── setup.py                  # Package setup
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔧 Development

### Code Formatting
The project uses Black for code formatting:
```bash
black lung_diseases_classification.py
```

### Linting
Run pylint to check code quality:
```bash
pylint lung_diseases_classification.py
```

### Type Checking
Run mypy for type checking:
```bash
mypy lung_diseases_classification.py
```
