# File 1: revig_cipher.py
import streamlit as st

class ReVigCipher:
    def __init__(self, key):
        self.key = key.upper()
        self.rev_key = key[::-1].upper()
    
    def _transform(self, text, mode):
        result = []
        key_idx = 0
        for i, char in enumerate(text):
            if not char.isalpha():
                result.append(char)
                continue
            
            base = ord('A') if char.isupper() else ord('a')
            key_char = self.key[key_idx % len(self.key)] if i % 2 == 0 else self.rev_key[key_idx % len(self.key)]
            key_shift = ord(key_char) - ord('A')
            
            if mode == 'decrypt':
                key_shift = -key_shift
                
            result.append(chr((ord(char) - base + key_shift) % 26 + base))
            key_idx += 1
        
        return ''.join(result)
    
    def encrypt(self, plaintext):
        return self._transform(plaintext, 'encrypt')
    
    def decrypt(self, ciphertext):
        return self._transform(ciphertext, 'decrypt')

# Streamlit App
def revig_app():
    st.title("🔁 ReVig Cipher")
    operation = st.radio("Select operation:", ("Encrypt", "Decrypt"))
    key = st.text_input("Enter key (letters only):", value="SECRET")
    text = st.text_area(f"Enter text to {operation.lower()}:")
    
    if st.button(f"{operation}"):
        cipher = ReVigCipher(key)
        if operation == "Encrypt":
            result = cipher.encrypt(text)
        else:
            result = cipher.decrypt(text)
        st.subheader("Result:")
        st.code(result)