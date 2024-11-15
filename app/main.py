import socket
import threading

valid_path = ['/', '/echo', '/index.html', '/user-agent']

def client_handle(client_socket):
    try:
        client_req_encode = client_socket.recv(4096)
        client_req_decode = client_req_encode.decode()
        split_req = client_req_decode.split()

        path = split_req[1]

        if 'echo' in path:
            path = path.replace('/echo/', '')
            response_body = path
            content_length = len(path)
            response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
        elif 'user-agent' in path:
            path = split_req[6]
            response_body = path
            content_length = len(path)
            response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
        elif path == '/':
            response_ok = (f'HTTP/1.1 200 OK\r\n\r\n').encode()
        else:
            path = path.replace('/', '')
            response_body = path
            content_length = len(path)
            response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
        
        response_failed = ('HTTP/1.1 404 Not Found\r\n\r\n').encode()

        if split_req[1] in valid_path or split_req[1].startswith('/echo'):
            client_socket.send(response_ok)
        else:
            client_socket.send(response_failed)

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Close the connection
        client_socket.close()



def main():
    # Create the server socket once
    server = socket.create_server(('localhost', 4221), reuse_port=True)
    print("Server running on localhost:4221...")

    while True:
        # Accept a new client connection
        client_socket, client_addr = server.accept()
        print(f"New connection from {client_addr}")

        # Create and start a new thread for the client
        client_thread = threading.Thread(target=client_handle, args=(client_socket,))
        client_thread.start()
        

main()