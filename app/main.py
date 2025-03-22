import socket
import struct

def main():
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    conn, addr = server.accept()
    print(f"Connected by {addr}")

    data = conn.recv(1024)
    
    if len(data) < 12:
        print("Not enough data received")
        conn.close()
        return

    offset = 4
    request_api_key = struct.unpack('>h', data[offset:offset + 2])[0]
    offset += 2

    request_api_version = struct.unpack('>h', data[offset:offset + 2])[0]
    offset += 2

    correlation_id = struct.unpack('>i', data[offset:offset + 4])[0]
    
    print(f"Request API version: {request_api_version}, correlation_id: {correlation_id}")
    
    if request_api_version < 0 or request_api_version > 4:
        error_code = 35  
    else:
        error_code = 0  

    message_size = 0  
    response = (
        struct.pack('>i', message_size) +
        struct.pack('>i', correlation_id) +
        struct.pack('>h', error_code)
    )
    
    conn.sendall(response)
    conn.close()

if __name__ == "__main__":
    main()
