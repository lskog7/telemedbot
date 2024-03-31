from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Hash import MD5
from Crypto import Random

def transform_password(password):
    h = MD5.new()
    h.update(password.encode())
    return h.digest()

def encrypt(message, key, iv):
    message = str(message)
    message_hash = SHA3_256.new(message.encode())
    message_with_hash = message.encode() + message_hash.hexdigest().encode()
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_message = iv + cipher.encrypt(message_with_hash)
    return encrypted_message.hex()


def decrypt(encr, key, iv):

    encr = bytes.fromhex(encr)

    bsize = AES.block_size
    dsize = SHA3_256.digest_size * 2

    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted_message_with_hesh = cipher.decrypt(encr)[bsize:]
    decrypted_message = decrypted_message_with_hesh[:-dsize]
    digest = SHA3_256.new(decrypted_message).hexdigest()
    try:
        decoding_decrypted_message = decrypted_message_with_hesh[-dsize:].decode()
    except UnicodeDecodeError:
        raise KeyError
    else:
        if digest == decoding_decrypted_message:
            return decrypted_message.decode()
