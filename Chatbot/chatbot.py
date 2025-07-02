from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import requests
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"  # Default Ollama URL
DEFAULT_MODEL = "llama2"  # Change to your preferred model


class OllamaStreamer:
    def __init__(self, base_url=OLLAMA_BASE_URL):
        self.base_url = base_url

    def stream_chat(self, model, messages, temperature=0.7, max_tokens=None):
        """
        Stream chat responses from Ollama
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
            }
        }

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        try:
            response = requests.post(
                url,
                json=payload,
                stream=True,
                timeout=60
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'message' in chunk and 'content' in chunk['message']:
                            content = chunk['message']['content']
                            if content:  # Only yield non-empty content
                                yield content

                        # Check if streaming is done
                        if chunk.get('done', False):
                            break

                    except json.JSONDecodeError as e:
                        logging.error(f"JSON decode error: {e}")
                        continue

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            yield f"Error: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            yield f"Error: {str(e)}"

    def generate_text(self, model, prompt, temperature=0.7, max_tokens=None):
        """
        Stream text generation from Ollama (alternative method)
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
            }
        }

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        try:
            response = requests.post(
                url,
                json=payload,
                stream=True,
                timeout=60
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'response' in chunk:
                            content = chunk['response']
                            if content:  # Only yield non-empty content
                                yield content

                        # Check if streaming is done
                        if chunk.get('done', False):
                            break

                    except json.JSONDecodeError as e:
                        logging.error(f"JSON decode error: {e}")
                        continue

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            yield f"Error: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            yield f"Error: {str(e)}"


# Initialize Ollama streamer
ollama = OllamaStreamer()

# Store conversation history (in production, use a database)
conversations = {}


@app.route('/health', methods=['GET'])
def health_check():
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


"""
@app.route('/models', methods=['GET'])
def get_models():
    Get available Ollama models
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        models = response.json()
        return jsonify(models)
    except Exception as e:
        return jsonify({"error": str(e)}), 500})
"""


@app.route('/chat', methods=['POST'])
def chat():
    """
    Stream chat responses
    Expected payload:
    {
        "message": "user message",
        "conversation_id": "optional_conversation_id",
        "model": "optional_model_name",
        "temperature": 0.7,
        "max_tokens": 1000,
        "system_prompt": "optional_system_prompt"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        conversation_id = data.get('conversation_id', 'default')
        model = data.get('model', DEFAULT_MODEL)
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens')
        system_prompt = data.get('system_prompt', 'You are a helpful assistant.')

        # Get or create conversation history
        if conversation_id not in conversations:
            conversations[conversation_id] = []

        # Add system message if this is the first message
        if not conversations[conversation_id]:
            conversations[conversation_id].append({
                "role": "system",
                "content": system_prompt
            })

        # Add user message to conversation
        conversations[conversation_id].append({
            "role": "user",
            "content": user_message
        })

        def generate():
            try:
                assistant_message = ""

                # Stream the response
                for chunk in ollama.stream_chat(
                        model=model,
                        messages=conversations[conversation_id],
                        temperature=temperature,
                        max_tokens=max_tokens
                ):
                    assistant_message += chunk
                    # Send chunk as Server-Sent Event
                    yield f"data: {json.dumps({'content': chunk, 'type': 'chunk'})}\n\n"

                # Add assistant message to conversation history
                conversations[conversation_id].append({
                    "role": "assistant",
                    "content": assistant_message
                })

                # Send completion signal
                yield f"data: {json.dumps({'type': 'done', 'full_message': assistant_message})}\n\n"

            except Exception as e:
                logging.error(f"Error in generate function: {e}")
                yield f"data: {json.dumps({'error': str(e), 'type': 'error'})}\n\n"

        return Response(
            generate(),
            mimetype='text/plain',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'  # Disable nginx buffering
            }
        )

    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/chat/simple', methods=['POST'])
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
            return jsonify({"error": "Prompt is required"}), 400

        model = data.get('model', DEFAULT_MODEL)
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens')

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





@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


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

    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=3000,
        debug=True,
        threaded=True
    )