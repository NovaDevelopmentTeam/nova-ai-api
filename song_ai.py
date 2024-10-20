import os
import shutil
import json
import uuid
from functools import wraps
import numpy as np
import librosa
from flask import Flask, request, jsonify, send_file, abort
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Path for the API keys file
API_KEYS_FILE = 'api_keys.json'

# Admin key (creator)
ADMIN_API_KEY = 'your_admin_key_here'  # Replace with a secure key

# Path to the generated music file (to be replaced with your actual music generation logic)
GENERATED_MUSIC_FILE = 'generated_music.wav'

# 1. Utility function to load API keys from JSON file
def load_api_keys():
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    return {}

# 2. Utility function to save API keys to JSON file
def save_api_keys(api_keys):
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, f)

# 3. Generate a new API key
def generate_api_key():
    return str(uuid.uuid4())

# 4. API key decorator for route protection
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        api_keys = load_api_keys()
        
        if api_key not in api_keys and api_key != ADMIN_API_KEY:
            return jsonify({'error': 'Invalid API key'}), 403
        return f(*args, **kwargs)
    return decorated_function

# 5. Generate and save new API key
@app.route('/generate_key', methods=['POST'])
def generate_key():
    # Check if the request contains the admin API key
    api_key = request.headers.get('x-api-key')
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Generate a new API key and save it
    new_api_key = generate_api_key()
    api_keys = load_api_keys()
    api_keys[new_api_key] = True  # True means active
    save_api_keys(api_keys)
    
    return jsonify({'message': 'API key generated', 'api_key': new_api_key})

# 6. List all API keys (admin only)
@app.route('/list_keys', methods=['GET'])
@require_api_key
def list_keys():
    # Check if the request contains the admin API key
    api_key = request.headers.get('x-api-key')
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403
    
    api_keys = load_api_keys()
    return jsonify({'api_keys': list(api_keys.keys())})

# 7. Delete an API key (admin only)
@app.route('/delete_key', methods=['POST'])
@require_api_key
def delete_key():
    api_key = request.headers.get('x-api-key')
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    key_to_delete = data.get('api_key')
    api_keys = load_api_keys()

    if key_to_delete in api_keys:
        del api_keys[key_to_delete]
        save_api_keys(api_keys)
        return jsonify({'message': 'API key deleted'})
    else:
        return jsonify({'error': 'API key not found'}), 404

# 8. Example protected route
@app.route('/protected_route', methods=['GET'])
@require_api_key
def protected_route():
    return jsonify({'message': 'You have accessed a protected route'})

# 9. Function to extract features from audio
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma.T, axis=0)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_mean = np.mean(spectral_contrast.T, axis=0)
    return np.hstack([mfcc_mean, chroma_mean, contrast_mean])

# 10. Process data from directory
def process_directory(directory, label):
    features = []
    labels = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".mp3") or file_name.endswith(".wav"):
            file_path = os.path.join(directory, file_name)
            try:
                features.append(extract_features(file_path))
                labels.append(label)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
    return features, labels

# 11. Create the neural network model
def create_model(input_shape, is_ai_music=False):
    model = Sequential()
    model.add(Dense(256, activation='relu', input_shape=input_shape))
    model.add(Dropout(0.3))
    if is_ai_music:
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
    else:
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# 12. Train the model
def train_model(X_train, y_train, X_test, y_test, is_ai_music=False):
    model = create_model((X_train.shape[1],), is_ai_music=is_ai_music)
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
    model_path = 'ai_music_classifier.h5' if not is_ai_music else 'ai_music_classifier_ai.h5'
    model.save(model_path)
    return model_path

# Flask route to upload folder
@app.route('/upload_folder', methods=['POST'])
@require_api_key
def upload_folder():
    if 'zipfile' not in request.files:
        return jsonify({'error': 'No folder provided'}), 400

    zipfile = request.files['zipfile']
    if zipfile.filename == '':
        return jsonify({'error': 'No folder selected'}), 400

    extract_dir = f'uploaded_data/{zipfile.filename.split(".")[0]}'
    os.makedirs(extract_dir, exist_ok=True)
    zip_path = os.path.join(extract_dir, zipfile.filename)
    zipfile.save(zip_path)
    shutil.unpack_archive(zip_path, extract_dir)
    os.remove(zip_path)

    return jsonify({'message': 'Folder uploaded and extracted', 'folder_path': extract_dir})

# Route to train AI model
@app.route('/train', methods=['POST'])
@require_api_key
def train():
    data = request.get_json()
    folder_path = data.get('folder_path')
    label_type = data.get('label_type')
    if not folder_path or not os.path.exists(folder_path):
        return jsonify({'error': 'Invalid folder path'}), 400

    label = 1 if label_type == 'ai' else 0
    features, labels = process_directory(folder_path, label)
    if len(features) == 0:
        return jsonify({'error': 'No valid audio files found in the folder'}), 400

    X_train, X_test, y_train, y_test = train_test_split(np.array(features), np.array(labels), test_size=0.2, random_state=42)
    is_ai_music = label == 1
    model_path = train_model(X_train, y_train, X_test, y_test, is_ai_music)
    shutil.rmtree(folder_path)
    return jsonify({'message': 'Training completed', 'model_path': model_path})

# Song generation route
@app.route('/generate', methods=['POST'])
@require_api_key
def generate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = f'temp_{file.filename}'
    file.save(file_path)

    # Placeholder for actual generation logic; the file should be generated here
    if os.path.exists(GENERATED_MUSIC_FILE):
        return send_file(GENERATED_MUSIC_FILE, as_attachment=True)
    else:
        return jsonify({'error': 'Generated music file not found'}), 500

# Cleanup after response
@app.after_request
def cleanup(response):
    file_to_delete = request.files.get('file')
    if file_to_delete:
        temp_file_path = f'temp_{file_to_delete.filename}'
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
