import socket  # noqa: F401
import re

def main():
    
    valid_path = ['/', '/index.html', '/echo/.*$']
    
    http_response_failed = b"HTTP/1.1 404 Not Found\r\n\r\n"
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()
    msg = client_socket.recv(4096) 
    decoded_msg = msg.decode()
    split_msg = decoded_msg.split('\r\n')
    request = split_msg[0]
    split_request = request.split()
    path = split_request[1]
    response_body = path.replace('/echo/', '')
    encode_body = response_body.encode()
    valid = False
    http_response_ok = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\n"
    final_res = http_response_ok + encode_body
    print(final_res)
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