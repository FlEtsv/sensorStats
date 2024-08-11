from cryptography.fernet import Fernet

class Encryptor:
    def __init__(self, key=None):
        if key is None:
            # Generate a new key if not provided
            self.key = Fernet.generate_key()
        else:
            # Ensure the key is in bytes
            self.key = key.encode('utf-8')
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        # Encrypt the data
        encrypted = self.cipher.encrypt(data.encode('utf-8'))
        return encrypted.decode('utf-8')

    def decrypt(self, encrypted_data):
        # Decrypt the data
        decrypted = self.cipher.decrypt(encrypted_data.encode('utf-8'))
        return decrypted.decode('utf-8')

    def is_encrypted(self, data):
        try:
            # Try to decrypt the data to check if it's encrypted
            self.cipher.decrypt(data.encode('utf-8'))
            return True
        except Exception:
            return False

    def verify(self, data, encrypted_data):
        # Encrypt the data and compare it to the encrypted data provided
        encrypted = self.encrypt(data)
        return encrypted == encrypted_data

# Ejemplo de uso
key = Fernet.generate_key().decode('utf-8')  # Genera una clave que puedes guardar para usar más tarde
encryptor = Encryptor(key)

mensaje = "Mensaje secreto"
mensaje_cifrado = encryptor.encrypt(mensaje)
print(f"Mensaje cifrado: {mensaje_cifrado}")

mensaje_descifrado = encryptor.decrypt(mensaje_cifrado)
print(f"Mensaje descifrado: {mensaje_descifrado}")
