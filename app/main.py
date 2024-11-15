import socket  # noqa: F401
import re

def main():
    
    valid_path = ['^/$', '^/index.html$', '^/echo/.*$']
    http_response_failed = b"HTTP/1.1 404 Not Found\r\n\r\n"
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()
    msg = client_socket.recv(4096) 
    decoded_msg = msg.decode()
    split_msg = decoded_msg.split('\r\n')
    request = split_msg[0]
    split_request = request.split()
    path = split_request[1]

    valid = False

    if path == '/user-agent':
        response_body = split_msg[3]
        response_body = response_body.split()
        response_body = response_body[1]
        encode_body = response_body.encode()
        length_content = len(response_body)
        valid = True
    elif path.startswith('/echo'):
        response_body = path.replace('/echo/', '')
        encode_body = response_body.encode()
        length_content = len(response_body)
        valid = True
        final_res = (
            f'HTTP/1.1 200 OK\r\n'
            f'Content-Type: text/plain\r\n'
            f'Content-Length: {length_content}\r\n'
            f'\r\n'
            ).encode() + encode_body
    elif path == '/index.html':
        response_body = path.replace('/', '')
        encode_body = response_body.encode()
        length_content = len(response_body)
        final_res = (
            f'HTTP/1.1 200 OK\r\n'
            f'Content-Type: text/plain\r\n'
            f'Content-Length: {length_content}\r\n'
            f'\r\n'
            ).encode() + encode_body
        valid = True
    elif path == '/':
        response_body = path.replace('/', '')
        encode_body = response_body.encode()
        length_content = len(response_body)
        final_res = (
            f'HTTP/1.1 200 OK\r\n'
            f'Content-Type: text/plain\r\n'
            f'Content-Length: {length_content}\r\n'
            f'\r\n'
            ).encode() + encode_body
        valid = True
    else:
        valid = False




  
    for item in valid_path:
  
        if re.match(item, path):
            
            client_socket.send(final_res)
            valid = True
            break
            

    if not valid:
            client_socket.send(http_response_failed)
    
    client_socket.close()
    
if __name__ == "__main__":
    main()