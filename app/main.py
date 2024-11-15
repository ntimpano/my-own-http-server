import socket  # noqa: F401
import re

def main():
    
    valid_path = ['^/$', '^/index.html$', '^/echo/.*$', '^/user-agent$']
    http_response_failed = b"HTTP/1.1 404 Not Found\r\n\r\n"

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()

    msg = client_socket.recv(4096) 
    decoded_msg = msg.decode()
    split_msg = decoded_msg.split('\r\n')

    if len(split_msg) > 2:
         path = split_msg[2].split()[1]
         response_body = path
         encode_body = response_body.encode()
         length_content = len(response_body)
         encode_body = response_body.encode()
    
    elif len(split_msg) > 1 < 2: 
         request = split_msg[0]
         split_request = request.split()
         path = split_request[1]
         response_body = path.replace('/echo/', '')
         encode_body = response_body.encode()
         length_content = len(response_body)


    #request = split_msg[0]
    #split_request = request.split()
    #path = split_request[1]
    #response_body = path.replace('/echo/', '')
    #encode_body = response_body.encode()
    #length_content = len(response_body)
    #usr_agent_path = split_msg[2].split()[1]
    #usr_length = len(usr_agent_path)
    #usr_agent_path_encode = usr_agent_path.encode()

    
    #print(f'hola nahuel {split_request}')
    #print(f'hola nahuel {length_content}')

    final_res = (
         f'HTTP/1.1 200 OK\r\n'
         f'Content-Type: text/plain\r\n'
         f'Content-Length: {length_content}\r\n'
         f'\r\n'
    ).encode() + encode_body


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