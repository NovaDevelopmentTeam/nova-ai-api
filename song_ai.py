import os
import shutil
import numpy as np
import librosa
from flask import Flask, request, jsonify, send_file
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model

app = Flask(__name__)

# 1. Extract Features from Audio using LibROSA
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)

    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)

    # Extract Chroma features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma.T, axis=0)

    # Extract Spectral Contrast
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_mean = np.mean(spectral_contrast.T, axis=0)

    # Combine the features into a single feature vector
    return np.hstack([mfcc_mean, chroma_mean, contrast_mean])

# 2. Load and Process Data from Directories
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

# Train the model for both types of music
def train_model(X_train, y_train, X_test, y_test, is_ai_music=False):
    model = create_model((X_train.shape[1],), is_ai_music=is_ai_music)
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
    model_path = 'ai_music_classifier.h5' if not is_ai_music else 'ai_music_classifier_ai.h5'
    model.save(model_path)
    return model_path

# Function to create the Neural Network model
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

    model.add(Dense(1, activation='sigmoid'))  # Binary classification (AI vs Human)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Function to classify new songs
def classify_song(audio_file):
    model = load_model('ai_music_classifier.h5')
    features = extract_features(audio_file).reshape(1, -1)
    prediction = model.predict(features)
    return "AI-generated" if prediction > 0.5 else "Human-composed"

# 3. Flask API to upload a folder for training
@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    if 'zipfile' not in request.files:
        return jsonify({'error': 'No folder provided'}), 400

    zipfile = request.files['zipfile']
    if zipfile.filename == '':
        return jsonify({'error': 'No folder selected'}), 400

    # Create a directory to store the extracted files
    extract_dir = f'uploaded_data/{zipfile.filename.split(".")[0]}'
    os.makedirs(extract_dir, exist_ok=True)
    
    # Save and extract the zipfile containing audio files
    zip_path = os.path.join(extract_dir, zipfile.filename)
    zipfile.save(zip_path)

    shutil.unpack_archive(zip_path, extract_dir)  # Unzip the file
    os.remove(zip_path)  # Remove the zip file after extraction

    return jsonify({'message': 'Folder uploaded and extracted', 'folder_path': extract_dir})

# 4. API endpoint to train the model with uploaded folder data
@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    folder_path = data.get('folder_path')
    label_type = data.get('label_type')  # 1 for AI music, 0 for human-composed
    
    if not folder_path or not os.path.exists(folder_path):
        return jsonify({'error': 'Invalid folder path'}), 400

    label = 1 if label_type == 'ai' else 0
    features, labels = process_directory(folder_path, label)

    if len(features) == 0:
        return jsonify({'error': 'No valid audio files found in the folder'}), 400

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(np.array(features), np.array(labels), test_size=0.2, random_state=42)

    # Train the model based on the label type
    is_ai_music = label == 1
    model_path = train_model(X_train, y_train, X_test, y_test, is_ai_music)

    # Optionally, delete folder after training to save space
    shutil.rmtree(folder_path)

    return jsonify({'message': 'Training completed', 'model_path': model_path})

# 5. API endpoint to generate a song (dummy logic for now)
@app.route('/generate', methods=['POST'])
def generate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the file temporarily
    file_path = f'temp_{file.filename}'
    file.save(file_path)

    # Dummy logic for generating new song
    generated_file_path = 'generated_music.wav'  # Dummy file for now

    # Return the generated file for download
    return send_file(generated_file_path, as_attachment=True)

# Ensure files are deleted after being used or on disconnect
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
