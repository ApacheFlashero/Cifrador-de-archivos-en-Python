import logging
import os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Hash import SHA512
from Crypto import Random
from Crypto.Random import get_random_bytes

def Instrucciones():
    print("Bienvenido al cifrador de archivos!")
    print("Instrucciones:")
    print("1- Insertar el nombre del archivo.")
    print("2- C para cifrar.")
    print("3- D para descifrar.")

# Cifrar
def Encrypt(key, filename):
    chunksize = 64 * 1024
    outputExtension = ".bin"
    outputFile = filename + outputExtension
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile: # Abrir el archivo como lectura
        with open(outputFile, 'wb') as outfile: # Activar modo escritura
            outfile.write(filesize.encode('UTF-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))
                
                outfile.write(encryptor.encrypt(chunk))

# Descifrar
def Decrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = filename[:11]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

# Contraseña
def getKey(password):
    hasher = SHA256.new(password.encode('UTF-8'))
    return hasher.digest()

def Main():
    Instrucciones()
    choice = input("Quieres (C)ifrar o (D)escifrar?: ")

    if choice == "C":
        filename = input("Archivo a cifrar: ")
        password = input("Contraseña: ")
        Encrypt(getKey(password), filename)
        print("Hecho.")
        
    elif choice == "D":
        filename = input("Archivo a descifrar: ")
        password = input("Contraseña: ")
        Decrypt(getKey(password), filename)
        print("Hecho.")
        
    else:
        print("Opción incorrecta, cerrando...")

if __name__ == '__main__':
    Main()
