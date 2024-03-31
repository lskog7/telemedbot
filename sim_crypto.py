from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Hash import MD5
from Crypto import Random

def transform_password(password):
    h = MD5.new()
    h.update(password.encode('utf-8'))
    return h.digest()

def encrypt(message, key):
    encr_key = transform_password(key)
    message_hash = SHA3_256.new(message.encode())
    message_with_hash = message.encode() + message_hash.hexdigest().encode()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(encr_key, AES.MODE_CFB, iv)
    encrypted_message = iv + cipher.encrypt(message_with_hash)
    return encrypted_message.hex()


def decrypt(encr, key):

    encr = bytes.fromhex(encr)
    decrypt_key = transform_password(key)

    bsize = AES.block_size
    dsize = SHA3_256.digest_size * 2

    iv = Random.new().read(bsize)
    cipher = AES.new(decrypt_key, AES.MODE_CFB, iv)
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


# if __name__ == '__main__':
#     text = 'fgjskdghk'
#     key1 = 'Traveling through hyperspace ain’t like dusting crops, farm boy regergergergerger.'
#     encr_message = encrypt(text, key1)
#     print(encr_message)
#     decr_message = decrypt(encr_message, key1)
#     print(decr_message)
#     print('------------------------------------------------')
#     key2 = 'I love it, I love it, I love it, I love it'
#     encr_message = encrypt(text, key2)
#     print(encr_message)
#     decr_message = decrypt(encr_message, key2)
#     print(decr_message)
#
#     print(decrypt(encr_message, key1))