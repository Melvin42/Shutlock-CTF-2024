import socket
import base64
import os
import threading
import random

# Dictionnary of images and their categories
images_files = {
    "dop_Cocaine.jpg": "dopante",
    "dop_Spice.jpg": "dopante",
    "dop_Alcohol.jpg": "dopante",
    "dop_Cannabis.jpg": "dopante",
    "dop_Heroin.jpg": "dopante",


    "Acetaminophen.png": "non-dopante",
    "Cephalexin.png": "non-dopante",
    "Ibuprofen.png": "non-dopante",
    "Amlodipine.png": "non-dopante",
    "Ciprofloxacin.png": "non-dopante"
}

ADDRESS = os.getenv('ADDRESS', '0.0.0.0')
PORT = int(os.getenv('PORT', 4444))

NUMBER_OF_CONNECTIONS = 5

def read_image(file_path):
    with open(file_path, "rb") as img_file:
        return img_file.read()


def handle_client(connection):
    try:
        print('Connexion de ', connection.getpeername())

        # Receive the go signal from the client
        data = connection.recv(1024)
        print(data)
        if data.decode().strip() == 'go':
            score = 0

            # Shuffle the images before sending them to the client
            shuffled_keys = list(images_files.keys())
            random.shuffle(shuffled_keys)
            shuffled_image_files = {key: images_files[key] for key in shuffled_keys}

            # Send the images to the client
            for image_name, category in shuffled_image_files.items():
                image_path = os.path.join(IMAGES_FOLDER, image_name)
                connection.settimeout(5)
                try:
                    # read the image
                    img_data = read_image(image_path)

                    # Encode the image in base64
                    encoded_img = base64.b64encode(img_data).decode('utf-8')

                    # First : send the size of the image
                    connection.sendall(str(len(encoded_img)).encode())

                    # Wait for the client to confirm the reception of the size
                    confirmation = connection.recv(1024)
                    if confirmation.decode() == 'ack':

                        # Send encoded image
                        connection.sendall(encoded_img.encode())
                        if connection.recv(1024).decode() == category:
                            print(f"Image {image_name} has been correctly classified as {category}")
                            score += 1
                        else:
                            print(f"Image {image_name} has been incorrectly classified as {category}")
                except socket.timeout:
                    print('Timeout, closing connection...')
                    connection.sendall('Timeout, Tu dois etre plus rapide!! '.encode())
                    connection.close()
                    return

            # Send the finish signal
            connection.sendall('finish '.encode())

            # Send the score to the client Or the flag if the score is > 80%
            if (score * 100 / len(images_files)) >= 80:
                print((score * 100)/len(images_files))
                connection.sendall(f"FLAG{{REDACTED}}".encode())
            else:
                connection.sendall(f"Ton Score est de : {score} * {100}/{len(images_files)} !!! Try Again".encode())
    finally:
        connection.close()



# Folder containing the images
IMAGES_FOLDER = 'images/general'

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = (ADDRESS, PORT)
print('The server running on {} port {}'.format(*server_address))
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(NUMBER_OF_CONNECTIONS)

def main():
    while True:
        # wait for a connection
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(connection,))
        client_thread.start()

if __name__ == "__main__":
    main()
