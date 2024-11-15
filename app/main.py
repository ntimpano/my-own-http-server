import socket


valid_path = ['/', '/echo', '/index.html', '/user-agent']

def main():
    while True:
        server = socket.create_server(('localhost', 4221), reuse_port=True)
        client_socket, client_addr = server.accept() 

        client_req_encode = client_socket.recv(4096)
        client_req_decode = client_req_encode.decode()

        split_req = client_req_decode.split()

        path = split_req[1] #esto es donde quiero acceder el usuario. Ej: localhost/index.html

        if 'echo' in path:
            path = path.replace('/echo/', '')
            response_body = path
            content_length = len(path)
        elif 'user-agent' in path:
            path = split_req[6]
            response_body = path
            content_length = len(path)
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

        client_socket.close()
        

main()