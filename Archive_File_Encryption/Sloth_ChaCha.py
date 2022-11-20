from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes
import base64
import secrets
import os
import hashlib
def en_file(filename,salt,key):
    BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once
    
    input_filename = filename  # Any file extension will work
    output_filename = input_filename + '.Cha.SafeSloth'  # You can name this anything, I'm just putting .encrypted on the end

    file_in = open(input_filename, 'rb')  # rb = read bytes. Required to read non-text files
    file_out = open(output_filename, 'wb')  # wb = write bytes. Required to write the encrypted data

    file_out.write(salt)  # Write the salt to the top of the output file
    nonce = get_random_bytes(24)
    file_out.write(nonce)  # Write out the nonce to the output file under the salt
    #print(cipher.nonce)
    aad = get_random_bytes(32)
    file_out.write(aad)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)# Create a cipher object to encrypt data
    cipher.update(aad)

# Read, encrypt and write the data
    data = file_in.read(BUFFER_SIZE)  # Read in some of the file
    while len(data) != 0:  # Check if we need to encrypt anymore data
        encrypted_data = cipher.encrypt(data)  # Encrypt the data we read
        file_out.write(encrypted_data)  # Write the encrypted data to the output file
        data = file_in.read(BUFFER_SIZE)  # Read some more of the file to see if there is any more left

# Get and write the tag for decryption verification
    tag = cipher.digest()  # Signal to the cipher that we are done and get the tag
    file_out.write(tag)

# Close both files
    file_in.close()
    file_out.close()

def de_file(filename,key):
    BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once


    input_filename = filename+'.Cha.SafeSloth'  # The encrypted file
    output_filename = filename  # The decrypted file

# Open files
    file_in = open(input_filename, 'rb')
    file_out = open(output_filename, 'wb')

# Read salt and generate key
    salt = file_in.read(32)  # Only to continue here, The salt we generated was 32 bits long

# Read nonce and create cipher
    nonce = file_in.read(24)  # The nonce is 16 bytes long
    aad = file_in.read(32)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    cipher.update(aad)

# Identify how many bytes of encrypted there is
# We know that the salt (32) + the nonce (16) + the data (?) + the tag (16) is in the file
# So some basic algebra can tell us how much data we need to read to decrypt
    file_in_size = os.path.getsize(input_filename)
    encrypted_data_size = file_in_size - 104  # Total - salt - nonce - tag = encrypted data

# Read, decrypt and write the data
    for _ in range(int(encrypted_data_size / BUFFER_SIZE)):  # Identify how many loops of full buffer reads we need to do
        data = file_in.read(BUFFER_SIZE)  # Read in some data from the encrypted file
        decrypted_data = cipher.decrypt(data)  # Decrypt the data
        file_out.write(decrypted_data)  # Write the decrypted data to the output file
    data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))  # Read whatever we have calculated to be left of encrypted data
    decrypted_data = cipher.decrypt(data)  # Decrypt the data
    file_out.write(decrypted_data)  # Write the decrypted data to the output file

# Verify encrypted file was not tampered with
    tag = file_in.read(16)
    try:
        cipher.verify(tag)
    except ValueError as e:
        # If we get a ValueError, there was an error when decrypting so delete the file we created
        file_in.close()
        file_out.close()
        os.remove(output_filename)
        raise e

# If everything was ok, close the files
    file_in.close()
    file_out.close()
