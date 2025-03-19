import socket
import struct


def main():
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    conn, _ = server.accept() 

    _ = conn.recv(1024)
    
    message_size = struct.pack('>i', 0)  # 4 bytes (big-endian) for message_size
    correlation_id = struct.pack('>i', 7)  # 4 bytes (big-endian) for correlation_id
    response = message_size + correlation_id
    
    conn.sendall(response)  
    conn.close()

if __name__ == "__main__":
    main()
