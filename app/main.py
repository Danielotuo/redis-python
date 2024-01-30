import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    print("Server listening on localhost:6379")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Handle the client in a separate thread or process if needed
        handle_client(client_socket)


def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)  # Adjust the buffer size as needed

        # Check if the client has closed the connection
        if not data:
            break

        # For simplicity, respond with +PONG\r\n for any input
        response = b"+PONG\r\n"
        client_socket.sendall(response)

    # Close the client socket when the communication is done
    client_socket.close()


if __name__ == "__main__":
    main()
