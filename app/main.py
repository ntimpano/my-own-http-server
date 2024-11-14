import socket  # noqa: F401


def main():
    print("Logs from your program will appear here!")
    
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()
    http_response = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"
    client_socket.sendall(http_response)
    client_socket.close()
    
if __name__ == "__main__":
    main()
