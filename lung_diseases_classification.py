#!/usr/bin/env python3
"""
Lung Diseases Classification using Machine Learning and Deep Learning

This module provides functionality for classifying lung diseases from X-ray images
using various machine learning and deep learning approaches.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from PIL import Image

# TensorFlow/Keras imports
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import (
    GlobalAveragePooling2D, 
    Dense, 
    Dropout, 
    BatchNormalization,
    Reshape,
    multiply,
    Activation
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.regularizers import l2

# Scikit-learn imports
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix,
    roc_curve,
    auc
)
from sklearn.preprocessing import label_binarize

# XGBoost import
from xgboost import XGBClassifier


class LungDiseaseClassifier:
    """
    A comprehensive lung disease classification system using multiple approaches.
    """
    
    def __init__(self, data_path: str = None):
        """
        Initialize the classifier.
        
        Args:
            data_path (str): Path to the dataset directory
        """
        self.data_path = data_path
        self.models = {}
        self.history = {}
        
    def setup_data_generators(self, 
                              image_size: tuple = (224, 224),
                              batch_size: int = 32,
                              validation_split: float = 0.2):
        """
        Set up data generators for training and validation.
        
        Args:
            image_size (tuple): Target image size
            batch_size (int): Batch size for training
            validation_split (float): Fraction of data for validation
        """
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            validation_split=validation_split
        )
        
        if self.data_path and os.path.exists(self.data_path):
            self.train_generator = train_datagen.flow_from_directory(
                self.data_path,
                target_size=image_size,
                batch_size=batch_size,
                class_mode='categorical',
                subset='training'
            )
            
            self.validation_generator = train_datagen.flow_from_directory(
                self.data_path,
                target_size=image_size,
                batch_size=batch_size,
                class_mode='categorical',
                subset='validation'
            )
        else:
            print("Warning: Data path not found or not provided.")
            
    def build_inception_model(self, 
                              num_classes: int = 3,
                              input_shape: tuple = (224, 224, 3)):
        """
        Build a transfer learning model using InceptionV3.
        
        Args:
            num_classes (int): Number of output classes
            input_shape (tuple): Input image shape
            
        Returns:
            tensorflow.keras.models.Model: Compiled model
        """
        # Load pre-trained InceptionV3 model
        base_model = InceptionV3(
            weights='imagenet',
            include_top=False,
            input_shape=input_shape
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom classification layers
        x = GlobalAveragePooling2D()(base_model.output)
        x = BatchNormalization()(x)
        x = Dense(512, activation='relu', kernel_regularizer=l2(0.01))(x)
        x = Dropout(0.5)(x)
        x = Dense(256, activation='relu', kernel_regularizer=l2(0.01))(x)
        x = Dropout(0.5)(x)
        predictions = Dense(num_classes, activation='softmax')(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss=CategoricalCrossentropy(),
            metrics=['accuracy']
        )
        
        self.models['inception'] = model
        return model
        
    def train_inception_model(self, 
                              epochs: int = 50,
                              patience: int = 10):
        """
        Train the InceptionV3 model.
        
        Args:
            epochs (int): Maximum number of training epochs
            patience (int): Early stopping patience
        """
        if 'inception' not in self.models:
            self.build_inception_model()
            
        if not hasattr(self, 'train_generator'):
            print("Error: Data generators not set up. Call setup_data_generators first.")
            return
            
        # Early stopping callback
        early_stopping = EarlyStopping(
            monitor='val_accuracy',
            patience=patience,
            restore_best_weights=True
        )
        
        # Train the model
        history = self.models['inception'].fit(
            self.train_generator,
            validation_data=self.validation_generator,
            epochs=epochs,
            callbacks=[early_stopping]
        )
        
        self.history['inception'] = history
        
    def build_traditional_ml_models(self):
        """
        Build traditional machine learning models (SVM, Random Forest, XGBoost).
        """
        self.models['svm'] = SVC(kernel='rbf', probability=True)
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        self.models['xgboost'] = XGBClassifier(
            n_estimators=100,
            random_state=42
        )
        
    def plot_training_history(self, model_name: str = 'inception'):
        """
        Plot training history for a given model.
        
        Args:
            model_name (str): Name of the model to plot history for
        """
        if model_name not in self.history:
            print(f"No training history found for model: {model_name}")
            return
            
        history = self.history[model_name]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot accuracy
        ax1.plot(history.history['accuracy'], label='Training Accuracy')
        ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        # Plot loss
        ax2.plot(history.history['loss'], label='Training Loss')
        ax2.plot(history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
        
    def evaluate_model(self, model_name: str, test_data=None):
        """
        Evaluate a trained model.
        
        Args:
            model_name (str): Name of the model to evaluate
            test_data: Test data for evaluation
        """
        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return
            
        model = self.models[model_name]
        
        # Use validation data if test data not provided
        if test_data is None and hasattr(self, 'validation_generator'):
            test_data = self.validation_generator
            
        if test_data is None:
            print("No test data available for evaluation.")
            return
            
        # Make predictions
        predictions = model.predict(test_data)
        
        # Calculate accuracy and other metrics
        # This would need to be adapted based on the specific data format
        print(f"Evaluation results for {model_name}:")
        # Add specific evaluation metrics here
        
    def plot_confusion_matrix(self, y_true, y_pred, class_names=None):
        """
        Plot confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            class_names: List of class names
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=class_names, yticklabels=class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.show()


def main():
    """
    Main function to demonstrate the usage of the classifier.
    """
    # Initialize classifier
    classifier = LungDiseaseClassifier()
    
    # Example usage (would need actual data path)
    # classifier.setup_data_generators()
    # classifier.build_inception_model()
    # classifier.train_inception_model()
    
    print("Lung Disease Classifier initialized successfully!")
    print("To use this classifier:")
    print("1. Set the data path when initializing")
    print("2. Call setup_data_generators()")
    print("3. Build and train models as needed")


if __name__ == "__main__":
    main()