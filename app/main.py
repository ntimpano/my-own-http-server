import socket  # noqa: F401


def main():
    print("Logs from your program will appear here!")
    
    http_response = ("HTTP/1.1 200 OK\r\n\r\n")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept()
    server_socket.sendall(http_response.encode())




if __name__ == "__main__":
    main()
