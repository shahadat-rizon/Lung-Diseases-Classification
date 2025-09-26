"""
Flask Web Application for Lung Disease Classification
Allows users to upload X-ray images and get predictions.
"""

import os
import json
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import tensorflow as tf
from model import load_or_create_model, predict_image, preprocess_image
import numpy as np
from PIL import Image
import io
import base64

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'lung_disease_classification_secret_key'  # Change in production

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model globally (initialize once)
print("Loading model...")
model = None

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file_path):
    """Validate that the uploaded file is a valid image"""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and prediction"""
    global model
    
    # Check if file was uploaded
    if 'file' not in request.files:
        flash('No file uploaded')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    # Check file extension
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.')
        return redirect(request.url)
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Validate image
        if not validate_image(file_path):
            os.remove(file_path)  # Clean up
            flash('Invalid image file. Please upload a valid image.')
            return redirect(request.url)
        
        # Load model if not already loaded
        if model is None:
            model = load_or_create_model()
        
        # Make prediction
        result = predict_image(model, file_path)
        
        # Convert image to base64 for display
        with open(file_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return render_template('result.html', 
                             result=result, 
                             image_data=img_data,
                             filename=filename)
    
    except Exception as e:
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        flash(f'Error processing image: {str(e)}')
        return redirect(request.url)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    global model
    
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Validate image
        if not validate_image(file_path):
            os.remove(file_path)
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Load model if not already loaded
        if model is None:
            model = load_or_create_model()
        
        # Make prediction
        result = predict_image(model, file_path)
        
        # Clean up
        os.remove(file_path)
        
        return jsonify(result)
    
    except Exception as e:
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File too large. Maximum size is 16MB.')
    return redirect(request.url)

if __name__ == '__main__':
    print("Starting Lung Disease Classification Web Application...")
    print("Note: This app uses a model that needs to be trained first for accurate predictions.")
    app.run(debug=True, host='0.0.0.0', port=5000)