# Librerias
import sys
import hashlib, hmac
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from binascii import hexlify
from cryptography.fernet import Fernet

# Datos
output_file = b'hash.bin' # Aqui cambias el texto al que quieras hashear (No cambies la extensión)
data = input("INSERTE TEXTO: ").encode()
keyAES = get_random_bytes(32)
key = get_random_bytes(512)
key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(data)

# Hash y AES
cipher = AES.new(keyAES, AES.MODE_EAX)
ciphered_data, tag = cipher.encrypt_and_digest(data)
sha = hashlib.sha3_512(data + token + key)
sha_hex_digest = sha.hexdigest()
hmac_code = hmac.new(key=key, msg=data, digestmod=hashlib.sha3_512)
hmac_hexdigest = hmac_code.hexdigest() 

# Archivo
file_out = open(output_file, 'wb').write()
file_out.write(cipher.nonce)
file_out.write(tag)
file_out.write(sha_hex_digest)
file_out.write(hmac_hexdigest)
file_out.write(ciphered_data)
file_out.close()