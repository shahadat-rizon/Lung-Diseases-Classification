"""
Simplified model implementation for demonstration purposes.
This version works without TensorFlow and provides mock predictions.
In production, replace this with the actual trained model.
"""

import os
import random
import hashlib
from typing import Dict, Any

# Define class names (same as in the original model)
CLASS_NAMES = {0: 'Lung Opacity', 1: 'Normal', 2: 'Viral Pneumonia'}
CLASS_LABELS = ['Lung Opacity', 'Normal', 'Viral Pneumonia']
NUM_CLASSES = 3

def validate_image_simple(img_path: str) -> bool:
    """
    Simple image validation without PIL.
    Checks file extension and basic file properties.
    """
    if not os.path.exists(img_path):
        return False
    
    # Check file extension
    valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    _, ext = os.path.splitext(img_path.lower())
    if ext not in valid_extensions:
        return False
    
    # Check if file is not empty
    if os.path.getsize(img_path) == 0:
        return False
    
    # Basic header check for common image formats
    try:
        with open(img_path, 'rb') as f:
            header = f.read(10)
            # Check for common image signatures
            if (header.startswith(b'\x89PNG') or  # PNG
                header.startswith(b'\xFF\xD8') or  # JPEG
                header.startswith(b'GIF87a') or header.startswith(b'GIF89a') or  # GIF
                header.startswith(b'BM')):  # BMP
                return True
    except Exception:
        pass
    
    return False

def generate_deterministic_prediction(img_path: str) -> Dict[str, Any]:
    """
    Generate a deterministic prediction based on file characteristics.
    This ensures consistent results for the same image during demo.
    """
    # Use file name and size to generate consistent "predictions"
    filename = os.path.basename(img_path)
    filesize = os.path.getsize(img_path)
    
    # Create a hash from filename and filesize for consistency
    hash_input = f"{filename}_{filesize}".encode()
    hash_digest = hashlib.md5(hash_input).hexdigest()
    
    # Use hash to seed random generator for consistent results
    seed = int(hash_digest[:8], 16)
    random.seed(seed)
    
    # Generate realistic-looking probabilities
    # Ensure they sum to 1.0
    probs = [random.uniform(0.1, 0.9) for _ in range(NUM_CLASSES)]
    total = sum(probs)
    probs = [p/total for p in probs]
    
    # Find the class with highest probability
    predicted_class_idx = probs.index(max(probs))
    predicted_class = CLASS_NAMES[predicted_class_idx]
    confidence = probs[predicted_class_idx]
    
    return {
        'class': predicted_class,
        'confidence': float(confidence),
        'all_predictions': {
            CLASS_LABELS[i]: float(probs[i]) 
            for i in range(len(CLASS_LABELS))
        }
    }

def predict_image_simple(img_path: str) -> Dict[str, Any]:
    """
    Simple prediction function that works without ML libraries.
    This is for demonstration purposes only.
    """
    # Validate image
    if not validate_image_simple(img_path):
        raise ValueError("Invalid image file")
    
    # Generate mock prediction
    result = generate_deterministic_prediction(img_path)
    
    return result

class SimpleLungDiseaseModel:
    """
    Simple mock model class for demonstration.
    In production, this would be replaced with the actual trained model.
    """
    
    def __init__(self):
        self.model_loaded = True
        self.classes = CLASS_LABELS
    
    def predict(self, img_path: str) -> Dict[str, Any]:
        """Make a prediction on an image"""
        return predict_image_simple(img_path)
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model_loaded

def load_simple_model() -> SimpleLungDiseaseModel:
    """Load the simple model"""
    print("Loading simple demonstration model...")
    print("Note: This is a mock model for demonstration purposes.")
    print("In production, replace this with your trained TensorFlow model.")
    return SimpleLungDiseaseModel()

if __name__ == "__main__":
    # Test the simple model
    model = load_simple_model()
    print(f"Model loaded: {model.is_loaded()}")
    print(f"Model classes: {model.classes}")
    
    # Test with a dummy file path (won't work without an actual file)
    print("\nModel ready for predictions!")