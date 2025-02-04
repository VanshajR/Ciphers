import streamlit as st
import tensorflow as tf
import numpy as np
import string
import os

st.set_page_config(page_title="Cipher Suite", page_icon="🔒", layout="centered", initial_sidebar_state="auto")
st.sidebar.title("Cipher Suite")
app_mode = st.sidebar.selectbox("Choose Cipher", ["ReVig Cipher", "NeuralCipher"])

if app_mode == "ReVig Cipher":
    from revig_cipher import revig_app
    revig_app()
elif app_mode == "NeuralCipher":
    
    # Define character set (printable ASCII characters)
    CHARSET = string.printable
    CHAR2IDX = {c: i for i, c in enumerate(CHARSET)}
    IDX2CHAR = {i: c for i, c in enumerate(CHARSET)}
    Vocab_size = len(CHARSET)

    # Model file paths
    ENCRYPT_MODEL_PATH = os.path.join(os.getcwd(), "encrypt_model.h5")
    DECRYPT_MODEL_PATH = os.path.join(os.getcwd(), "decrypt_model.h5")

    # Load trained models
    def load_models():
        if os.path.exists(ENCRYPT_MODEL_PATH) and os.path.exists(DECRYPT_MODEL_PATH):
            encrypt_model = tf.keras.models.load_model(ENCRYPT_MODEL_PATH)
            decrypt_model = tf.keras.models.load_model(DECRYPT_MODEL_PATH)
            return encrypt_model, decrypt_model
        else:
            raise FileNotFoundError("Trained models not found! Please run 'train_cipher_models.py' first.")

    # Initialize models
    encrypt_model, decrypt_model = load_models()

    # Encryption function
    def encrypt(text):
        encrypted_text = ""
        for char in text:
            if char in CHAR2IDX:
                one_hot = np.zeros((1, Vocab_size))
                one_hot[0, CHAR2IDX[char]] = 1
                encrypted_vector = encrypt_model.predict(one_hot, verbose=0)
                encrypted_char_idx = np.argmax(encrypted_vector)
                encrypted_text += IDX2CHAR[encrypted_char_idx]
            else:
                encrypted_text += char  # Leave unknown characters as-is
        return encrypted_text

    # Decryption function
    def decrypt(text):
        decrypted_text = ""
        for char in text:
            if char in CHAR2IDX:
                one_hot = np.zeros((1, Vocab_size))
                one_hot[0, CHAR2IDX[char]] = 1
                decrypted_vector = decrypt_model.predict(one_hot, verbose=0)
                decrypted_char_idx = np.argmax(decrypted_vector)
                decrypted_text += IDX2CHAR[decrypted_char_idx]
            else:
                decrypted_text += char  # Leave unknown characters as-is
        return decrypted_text

# Streamlit UI
    st.title("🤖 Neural Network Cipher")
    st.write("A neural network-based encryption and decryption tool.")

    option = st.radio("Select Mode:", ("Encrypt", "Decrypt"))

    if option == "Encrypt":
        text = st.text_area("Enter text to encrypt:")
        if st.button("Encrypt Text"): 
            encrypted_result = encrypt(text)
            st.success(f"Encrypted Text: {encrypted_result}")

    elif option == "Decrypt":
        cipher_text = st.text_area("Enter encrypted text:")
        if st.button("Decrypt Text"): 
            decrypted_result = decrypt(cipher_text)
            st.success(f"Decrypted Text: {decrypted_result}")
