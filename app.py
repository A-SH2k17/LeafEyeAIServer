"""
import necessary libraries
"""
from pyexpat.errors import messages

from werkzeug.utils import secure_filename
import os
import random
import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
from preprocessing import preprocess_image
from data import DISEASE_CLASSES, DISEASE_RECOMMENDATIONS, DISEASE_DESCRIPTIONS
import fertRecomm
from fert import fertilizers
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import requests
import logging
from Chatbot.chatbot import OllamaStreamer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
app.config['UPLOAD_FOLDER']     = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Configure logging
logging.basicConfig(level=logging.INFO)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"  # Default Ollama URL
DEFAULT_MODEL = "LeafEye-Mistral7b"

# Initialize Ollama streamer
ollama = OllamaStreamer()

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
    df = fertRecomm.preprocess_data(data["input"])
    link_df = pd.read_csv("project_variables/Crop_English_Links.csv")
    link_df = link_df[link_df["Crop"] == data["input"][1]].reset_index()
    link = link_df["Link"][0]
    fert = fertRecomm.predict(df)
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

@app.route('/health', methods=['GET'])
def health_check_ollama():
    """Health check endpoint"""
    try:
        # Test Ollama connection
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            return jsonify({"status": "healthy", "ollama": "connected"})
        else:
            return jsonify({"status": "unhealthy", "ollama": "disconnected"}), 503
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


@app.route('/api/chat/simple', methods=['POST'])
def simple_chat():
    """
    Simple text generation endpoint (no conversation history)
    Expected payload:
    {
        "prompt": "user prompt",
        "model": "optional_model_name",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({"error": "Messages is required"}), 400

        print(data.get('messages'))
        model = data.get('model', DEFAULT_MODEL)
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens',1000)

        def generate():
            try:
                full_response = ""

                # Stream the response
                for chunk in ollama.generate_text(
                        model=model,
                        prompt=prompt,
                        temperature=temperature,
                        max_tokens=max_tokens
                ):
                    full_response += chunk
                    # Send chunk as Server-Sent Event
                    yield f"data: {json.dumps({'content': chunk, 'type': 'chunk'})}\n\n"

                # Send completion signal
                yield f"data: {json.dumps({'type': 'done', 'full_response': full_response})}\n\n"

            except Exception as e:
                logging.error(f"Error in simple generate function: {e}")
                yield f"data: {json.dumps({'error': str(e), 'type': 'error'})}\n\n"

        return Response(
            generate(),
            mimetype='text/plain',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )

    except Exception as e:
        logging.error(f"Error in simple chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat/generate', methods=['POST'])
def generate_chat():
    """
    Generate complete text response from Ollama without streaming
    Expected payload:
    {
        "prompt": "user prompt",
        "model": "optional_model_name",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        model = data.get('model', DEFAULT_MODEL)
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)

        try:
            full_response = ""

            # Collect all chunks into a complete response
            for chunk in ollama.generate_text(
                    model=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
            ):
                full_response += chunk

            return jsonify({
                "success": True,
                "response": full_response,
                "model": model,
                "prompt": prompt
            })

        except Exception as e:
            logging.error(f"Error generating text: {e}")
            return jsonify({
                "success": False,
                "error": f"Error generating text: {str(e)}"
            }), 500

    except Exception as e:
        logging.error(f"Error in generate chat endpoint: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    # Check if Ollama is running
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            models = response.json().get('models', [])
            if models:
                print(f"Available models: {[model['name'] for model in models]}")
            else:
                print("⚠️  No models found. Make sure you have pulled at least one model.")
        else:
            print("⚠️  Ollama is not responding properly")
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("Make sure Ollama is running with: ollama serve")
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
