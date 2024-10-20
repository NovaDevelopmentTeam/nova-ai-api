import os
import numpy as np
import librosa
from flask import Flask, request, jsonify
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

# 3. Directories for AI-generated and human-composed music
ai_music_dir = 'path_to_ai_music'   # Directory for AI-generated music
human_music_dir = 'path_to_human_music'  # Directory for human-composed music

# Extract features and labels from both directories
ai_features, ai_labels = process_directory(ai_music_dir, 1)   # Label 1 for AI
human_features, human_labels = process_directory(human_music_dir, 0) # Label 0 for human

# Combine all features and labels
X = np.array(ai_features + human_features)
y = np.array(ai_labels + human_labels)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Create and Train the Neural Network Model
def create_model(input_shape, is_ai_music=False):
    model = Sequential()
    model.add(Dense(256, activation='relu', input_shape=input_shape))
    model.add(Dropout(0.3))

    if is_ai_music:
        # For AI-generated music: add extra layers or modify dropout
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))  # Increased dropout for regularization
    else:
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))

    model.add(Dense(1, activation='sigmoid'))  # Binary classification (AI vs Human)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train the model for both types of music
def train_model(X_train, y_train, X_test, y_test):
    # First, classify songs to determine training approach
    model = create_model((X_train.shape[1],), is_ai_music=False)  # Assume default is human music
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
    model.save('ai_music_classifier.h5')

    # Check if AI music exists in training set
    if np.any(y_train == 1):  # If there are AI songs, adjust training
        model = create_model((X_train.shape[1],), is_ai_music=True)  # Create a model for AI music
        history_ai = model.fit(X_train[y_train == 1], y_train[y_train == 1], epochs=50, batch_size=32, validation_data=(X_test[y_test == 1], y_test[y_test == 1]))
        model.save('ai_music_classifier_ai.h5')

# Train the models
train_model(X_train, y_train, X_test, y_test)

# 5. Function to Classify New Songs
def classify_song(audio_file):
    model = load_model('ai_music_classifier.h5')  # Load the saved model
    features = extract_features(audio_file).reshape(1, -1)  # Extract features from new song
    prediction = model.predict(features)
    return "AI-generated" if prediction > 0.5 else "Human-composed"

# 6. Flask API Endpoint for Classification
@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the file temporarily
    file_path = f'temp_{file.filename}'
    file.save(file_path)

    # Classify the song
    result = classify_song(file_path)

    # Remove the temporary file after classification
    os.remove(file_path)

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
