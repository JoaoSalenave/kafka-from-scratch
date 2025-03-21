import socket
import struct

def main():
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    conn, addr = server.accept()
    print(f"Connected by {addr}")

    data = conn.recv(1024)
    
    if len(data) < 12:
        conn.close()
        return
    
    correlation_offset = 4 + 2 + 2
    correlation_id = struct.unpack('>i', data[correlation_offset:correlation_offset + 4])[0]
    print(f"Extracted correlation_id: {correlation_id}")
    
    response_message_size = 0 
    response = struct.pack('>i', response_message_size) + struct.pack('>i', correlation_id)
    
    conn.sendall(response)
    conn.close()

if __name__ == "__main__":
    main()
