"""
import necessary libraries
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import random
import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
from preprocessing import preprocess_image
from data import DISEASE_CLASSES, DISEASE_RECOMMENDATIONS, DISEASE_DESCRIPTIONS
import chatbot
from fert import fertilizers

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Loading the model


def load_model():
    print("Loading model...")
    model_out = tf.keras.models.load_model("MobileNetV2.keras")
    print("Model loaded")
    print(model_out.summary())
    return model_out


# Global variable for the model
model = load_model()







# Function to predict disease from an image


def predict_disease(image_path):

    preprocessed = preprocess_image(image_path)

    if preprocessed is None:
        return None

    preprocessed = np.expand_dims(preprocessed,axis=0)
    preprocessed = (preprocessed*255).astype(np.uint8)
    prediction = model.predict(preprocessed)




    mock_prediction_index = np.argmax(prediction)
    confidence = np.max(prediction)

    predicted_class = DISEASE_CLASSES[mock_prediction_index]

    # Get recommendations for the disease, if available
    recommendations = DISEASE_RECOMMENDATIONS.get(predicted_class, ["No specific recommendations available"])

    return {
        "disease": predicted_class,
        "confidence": float(confidence),
        "recommendations": recommendations,
        "description":DISEASE_DESCRIPTIONS[predicted_class]
    }


@app.route('/api/fertilizer', methods=['POST'])
def recommend_fert():
    data = request.get_json()
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415
    print(data)
    df = chatbot.preprocess_data(data["input"])
    link_df = pd.read_csv("project_variables/Crop_English_Links.csv")
    link_df = link_df[link_df["Crop"] == data["input"][1]].reset_index()
    link = link_df["Link"][0]
    fert = chatbot.predict(df)
    return jsonify({"fertilizer": fert, "description": fertilizers[fert], "link": link,"success":True})

@app.route('/api/detect', methods=['POST'])
def detect_disease():
    # Check if the post request has the file part
    print(request.files)
    if 'image' not in request.files:
        print("failed 1")
        return jsonify({
            "success": False,
            "message": "No image file provided"
        }), 400

    file = request.files['image']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print("failed 2")
        return jsonify({
            "success": False,
            "message": "No image selected"
        }), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            result = predict_disease(file_path)
            if result is None:
                print("failed 3")
                return jsonify({
                    "success": False,
                    "message": "Error in detecting disease please upload a suitable plant image"
                }), 500

            return jsonify({
                "success": True,
                "disease": result["disease"],
                "confidence": result["confidence"],
                "recommendations": result["recommendations"],
                "description": result["description"]
            })

        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error during disease detection: {str(e)}"
            }), 500
    print("failed 4")
    return jsonify({
        "success": False,
        "message": "File type not allowed"
    }), 400


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
