#!/usr/bin/python3
import base64

message = "VGhpcyBpcyB0b28gZWFzeQ=="
message2 = "VWtkc2EwbEliSFprVTBKdVdsaFJaMlJIYUhCamVVSjVZVmRrYjJSRU9EMD0="

def getDecodedBase64(message):
    return base64.b64decode(message).decode('ascii')

print("message1:", getDecodedBase64(message))
print("message2:", getDecodedBase64(getDecodedBase64(getDecodedBase64(message2)))) # Thrice decoded

def encodeImage(image):
    with open(image, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message

print(encodeImage('./image.png'))


base64_image = encodeImage('./image.png')
print(base64_image)

def getImageFromB64(b64_img):
    with open('decode_img.png', 'wb') as file_to_save:
        decoded_img_data = base64.b64decode(b64_img)  # fixed
        file_to_save.write(decoded_img_data)

getImageFromB64(base64_image)