"""
Lung Disease Classification Model
Based on the InceptionV3 architecture with custom dense layers and SE block.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import (
    GlobalAveragePooling2D, Dense, Dropout, BatchNormalization,
    Reshape, multiply
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.preprocessing import image
import os

# Define class names
CLASS_NAMES = {0: 'Lung Opacity', 1: 'Normal', 2: 'Viral Pneumonia'}
CLASS_LABELS = ['Lung Opacity', 'Normal', 'Viral Pneumonia']
NUM_CLASSES = 3
IMG_SIZE = (224, 224)

def se_block(input_tensor, ratio=16):
    """Squeeze-and-Excitation block implementation"""
    channel_axis = -1  # For 'channels_last'
    filters = input_tensor.shape[channel_axis]
    se = GlobalAveragePooling2D()(input_tensor)
    se = Reshape((1, 1, filters))(se)
    se = Dense(filters // ratio, activation='relu', kernel_initializer='he_normal', use_bias=False)(se)
    se = Dense(filters, activation='sigmoid', kernel_initializer='he_normal', use_bias=False)(se)
    return multiply([input_tensor, se])

def create_model():
    """Create the lung disease classification model"""
    # Load InceptionV3 base model
    base_model = InceptionV3(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Add SE block and custom layers
    x = se_block(base_model.output)
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu', kernel_regularizer=l2(0.001))(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu', kernel_regularizer=l2(0.001))(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    outputs = Dense(NUM_CLASSES, activation='softmax', kernel_regularizer=l2(0.001))(x)
    
    # Build model
    model = Model(inputs=base_model.input, outputs=outputs)
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def preprocess_image(img_path):
    """Preprocess image for model prediction"""
    # Load and resize image
    img = image.load_img(img_path, target_size=IMG_SIZE)
    # Convert to array
    img_array = image.img_to_array(img)
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize pixel values to [0,1]
    img_array = img_array / 255.0
    
    return img_array

def predict_image(model, img_path):
    """Predict lung disease class for an image"""
    # Preprocess image
    img_array = preprocess_image(img_path)
    
    # Make prediction
    predictions = model.predict(img_array)
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx]
    
    # Get class name
    predicted_class = CLASS_NAMES[predicted_class_idx]
    
    return {
        'class': predicted_class,
        'confidence': float(confidence),
        'all_predictions': {
            CLASS_LABELS[i]: float(predictions[0][i]) 
            for i in range(len(CLASS_LABELS))
        }
    }

def load_or_create_model(model_path='lung_disease_model.h5'):
    """Load existing model or create and return a new one"""
    if os.path.exists(model_path):
        print(f"Loading existing model from {model_path}")
        model = tf.keras.models.load_model(model_path, custom_objects={'se_block': se_block})
    else:
        print("Creating new model (no pre-trained weights)")
        model = create_model()
        print("Note: Model created but not trained. For production use, you need to train the model first.")
    
    return model

if __name__ == "__main__":
    # Create model for testing
    model = create_model()
    print("Model created successfully!")
    print(f"Model input shape: {model.input.shape}")
    print(f"Model output shape: {model.output.shape}")
    print(f"Total parameters: {model.count_params():,}")