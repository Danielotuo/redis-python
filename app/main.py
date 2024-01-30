import socket
import threading


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    print("Server listening on localhost:6379")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Create a new thread to handle the client
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_thread.start()


def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)  # Adjust the buffer size as needed

        # Check if the client has closed the connection
        if not data:
            break

        # Decode data from bytes to string
        command = data.decode('utf-8').strip()

        # For simplicity, respond to the ECHO command
        if command.startswith('*'):
            # Parse RESP array
            parts = command.split('\r\n')
            num_elements = int(parts[0][1:])
            elements = parts[1:-1]

            # Check if it's an ECHO command
            if num_elements == 3 and elements[1] == '$4' and elements[3] == '$3' and elements[2].lower() == 'echo':
                response = elements[4].encode('utf-8') + b"\r\n"
                client_socket.sendall(response)
            else:
                response = b"-ERR Unknown command\r\n"
                client_socket.sendall(response)
        else:
            response = b"-ERR Unknown command\r\n"
            client_socket.sendall(response)

    # Close the client socket when the communication is done
    client_socket.close()


if __name__ == "__main__":
    main()
