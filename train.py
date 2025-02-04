import tensorflow as tf
import numpy as np
import string
import os

# Define character set (printable ASCII characters)
CHARSET = string.printable
CHAR2IDX = {c: i for i, c in enumerate(CHARSET)}
IDX2CHAR = {i: c for i, c in enumerate(CHARSET)}
Vocab_size = len(CHARSET)

# Model file paths
ENCRYPT_MODEL_PATH = "encrypt_model.h5"
DECRYPT_MODEL_PATH = "decrypt_model.h5"

# Function to build a simple neural network
def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(Vocab_size,)),
        tf.keras.layers.Dense(Vocab_size, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return model

# Train models and save them
def train_and_save_models():
    encrypt_model = build_model()
    decrypt_model = build_model()

    data = np.eye(Vocab_size)  # One-hot encoding of characters
    shift = np.roll(data, shift=5, axis=0)  # Shift encoding for encryption

    print("Training encryption model...")
    encrypt_model.fit(data, shift, epochs=200, verbose=1)
    encrypt_model.save(ENCRYPT_MODEL_PATH)

    print("Training decryption model...")
    decrypt_model.fit(shift, data, epochs=200, verbose=1)  # Reverse training for decryption
    decrypt_model.save(DECRYPT_MODEL_PATH)

    print(f"Models saved as {ENCRYPT_MODEL_PATH} and {DECRYPT_MODEL_PATH}")

# Run training
if __name__ == "__main__":
    train_and_save_models()
