import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
from app.models import AlzheimersInfo


# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'NEW-Alzheimer_classification(DenseNet121)_trained.keras')
CLASS_LABELS = ['MildDemented', 'ModerateDemented', 'NonDemented', 'VeryMildDemented']
IMG_SIZE = 224

# Load model with error handling
try:
    alzheimers_model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load the model. Ensure the path is correct. Error: {e}")

def load_and_preprocess_image(img_path):
    if not os.path.isfile(img_path):
        raise ValueError(f"The file {img_path} does not exist.")
    if not img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError("Invalid file type. Please upload a PNG or JPEG image.")
    try:
        img = Image.open(img_path).resize((IMG_SIZE, IMG_SIZE))
        img_array = image.img_to_array(img) / 255.0  # Normalize
        return np.expand_dims(img_array, axis=0)
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")

def classify_alzheimers_stage(image_path):
    img_array = load_and_preprocess_image(image_path)
    print(f"Image Shape after preprocessing: {img_array.shape}")  # Debugging line
    
    predictions = alzheimers_model.predict(img_array)
    print(f"Model Prediction: {predictions}")  # Debugging line
    
    predicted_class_index = np.argmax(predictions)
    confidence_score = np.max(predictions) * 100  # Percentage
    
    predicted_class = CLASS_LABELS[predicted_class_index]
    print(f"Predicted Class: {predicted_class}, Confidence Score: {confidence_score}")  # Debugging line
    
    return predicted_class, confidence_score


def get_disease_info(disease_name):
    # Query the database for the disease information based on the class_name
    disease_info = AlzheimersInfo.query.filter_by(class_name=disease_name).first()

    # If no data is found, return default information
    if disease_info:
        return {
            'class_name': disease_info.class_name,  # Include class_name
            'stage': disease_info.stage,            # Include stage
            'description': disease_info.description, # Include description
            'causes': 'Causes information not available in the database',  # Assuming causes is not available
            'solutions': 'Solutions information not available in the database',  # Assuming solutions is not available
            'recommendations': disease_info.care_recommendations  # Include recommendations
        }
    else:
        # Return default information if no matching record is found
        return {
            'class_name': 'No information available',
            'stage': 'No information available',
            'description': 'No information available',
            'causes': 'No information available',
            'solutions': 'No information available',
            'recommendations': 'No information available'
        }