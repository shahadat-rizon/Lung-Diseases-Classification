# Lung-Diseases-Classification

A web application for lung disease classification using AI to analyze X-ray images and detect potential conditions.

## 🚀 Features

- **Web Interface**: Easy-to-use web application for X-ray image upload
- **AI Prediction**: Classifies lung X-rays into three categories:
  - **Normal**: Healthy lung conditions
  - **Lung Opacity**: Varying degrees of lung abnormalities  
  - **Viral Pneumonia**: Cases of viral pneumonia
- **Real-time Results**: Instant analysis with confidence scores
- **API Endpoint**: RESTful API for programmatic access
- **Responsive Design**: Works on desktop and mobile devices

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

## 🛠️ Installation & Setup

### Option 1: Simple Version (No Dependencies)
For demonstration purposes, you can run the simple version that doesn't require TensorFlow:

```bash
# Clone the repository
git clone https://github.com/shahadat-rizon/Lung-Diseases-Classification.git
cd Lung-Diseases-Classification

# Run the simple web application
python3 simple_app.py
```

Then open your browser and go to `http://localhost:5000`

### Option 2: Full Version (With TensorFlow)
For production use with the actual trained model:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full application
python3 app.py
```

## 🖥️ Usage

### Web Interface
1. Open your browser and navigate to `http://localhost:5000`
2. Click on the upload area or drag and drop an X-ray image
3. Click "Analyze Image" to get predictions
4. View results with confidence scores and detailed analysis

### API Usage
```bash
# Upload an image for analysis
curl -X POST -F "file=@your_xray_image.jpg" http://localhost:5000/api/predict

# Check server health
curl http://localhost:5000/health
```

## 📁 Project Structure

```
├── Lung Diseases Classification.ipynb  # Original Jupyter notebook with model training
├── app.py                             # Full Flask application (requires TensorFlow)
├── simple_app.py                      # Simple web server (no dependencies)
├── model.py                           # TensorFlow model implementation
├── simple_model.py                    # Mock model for demonstration
├── requirements.txt                   # Python dependencies
├── templates/                         # HTML templates
│   ├── base.html                     # Base template
│   ├── index.html                    # Upload page
│   └── result.html                   # Results page
└── README.md                         # This file
```

## 🧠 Model Architecture

The model is based on InceptionV3 with custom layers:
- **Base Model**: InceptionV3 (pre-trained on ImageNet)
- **Custom Layers**: 
  - Squeeze-and-Excitation (SE) block
  - Global Average Pooling
  - Dense layers with dropout and batch normalization
  - Output layer with 3 classes (softmax activation)

## ⚠️ Important Disclaimers

- **Educational Purpose**: This application is for educational and research purposes only
- **Not for Medical Diagnosis**: Always consult healthcare professionals for medical diagnosis
- **Mock Predictions**: The simple version uses mock predictions for demonstration
- **Model Training**: The full model requires training on the dataset for accurate predictions

## 🔧 Development

### Running Tests
```bash
# Test the simple model
python3 simple_model.py

# Test with a sample image
python3 -c "from simple_model import load_simple_model; model = load_simple_model(); print('Model ready!')"
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📊 Model Performance

The model architecture includes:
- Input size: 224x224x3
- Classes: 3 (Normal, Lung Opacity, Viral Pneumonia)
- Architecture: InceptionV3 + Custom Dense Layers
- Training: Transfer learning with fine-tuning

For detailed training results, see the Jupyter notebook.

## 📄 License

This project is for educational purposes. Please ensure proper attribution when using the dataset or code.

## 🤝 Acknowledgments

- Dataset from [Mendeley Data](https://data.mendeley.com/datasets/9d55cttn5h/1)
- InceptionV3 architecture from TensorFlow/Keras
- Bootstrap for UI components
