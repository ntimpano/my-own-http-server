import socket
import threading
import sys
import os

valid_path = ['/', '/echo', '/index.html', '/user-agent', '/files']
args = sys.argv


def client_handle(client_socket):
    try:
        client_req_encode = client_socket.recv(4096)
        client_req_decode = client_req_encode.decode()
        split_req = client_req_decode.split()

        path = split_req[1]

        print(f'DEBUG: {split_req}')
        
        if 'echo' in path:
            path = path.replace('/echo/', '')
            response_body = path
            content_length = len(path)  
            if 'Accept-Encoding:' in split_req:
                print(f'DEBUG: {split_req}')
                if split_req[6] != 'invalid-encoding':
                    encoding = split_req[6]
                    response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: {encoding}\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
                else:
                    response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
            else:
                response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
        elif 'user-agent' in path:
            path = split_req[6]
            response_body = path
            content_length = len(path)
            response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
        elif path == '/':
            response_ok = (f'HTTP/1.1 200 OK\r\n\r\n').encode()
        elif 'files' in path:
            dir_index = args.index('--directory') + 1
            dir = args[dir_index]
            file = path.replace('/files/', '')
            full_path = dir + file
            if 'GET' in split_req[0]:
                if os.path.isfile(full_path):
                    content_length = os.stat(full_path).st_size
                    content_type = 'application/octet-stream'
                    with open(full_path, 'r') as file_content:
                        response_body = file_content.read()
                    response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
                else:
                    response_ok = ('HTTP/1.1 404 Not Found\r\n\r\n').encode()
            elif 'POST' in split_req[0]:
                os.makedirs(dir, exist_ok=True)
                filename = os.path.basename(split_req[1])
                destination = os.path.join(dir, filename)
                with open(destination, 'w') as dst_file:
                    dst_file.write(client_req_decode.split('\r\n')[5])         
                response_ok = b'HTTP/1.1 201 Created\r\n\r\n'
                
        else:
            path = path.replace('/', '')
            response_body = path
            content_length = len(path)
            response_ok = (f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}').encode()
        
        response_failed = ('HTTP/1.1 404 Not Found\r\n\r\n').encode()

        if split_req[1] in valid_path or split_req[1].startswith('/echo') or split_req[1].startswith('/files'):
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

    while True:
        # Accept a new client connection
        client_socket, client_addr = server.accept()

        # Create and start a new thread for the client
        client_thread = threading.Thread(target=client_handle, args=(client_socket,))
        client_thread.start()
        

main()