from cryptography.fernet import Fernet
key = b'9KVCqB0JZI89XuF2wrbSJ1zP3GTVXQgRM2QKnKRpOlI='


def encrypt_id(id):
    cipher_suite = Fernet(key)
    encrypted_id = cipher_suite.encrypt(bytes(str(id), 'utf-8'))
    return encrypted_id.decode()


def decrypt_id(encrypted_id):
    cipher_suite = Fernet(key)
    decrypted_id = cipher_suite.decrypt(bytes(encrypted_id, 'utf-8'))
    return int(decrypted_id.decode())
