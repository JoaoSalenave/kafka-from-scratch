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
    _ = struct.unpack('>h', data[offset:offset + 2])[0]
    offset += 2

    _ = struct.unpack('>h', data[offset:offset + 2])[0]
    offset += 2

    correlation_id = struct.unpack('>i', data[offset:offset + 4])[0]
    
    throttle_time_ms = 0
    error_code = 0
    api_keys_count = 1
    api_entry = struct.pack('>h', 18) + struct.pack('>h', 0) + struct.pack('>h', 4)
    
    response_body = (
        struct.pack('>i', throttle_time_ms) +
        struct.pack('>h', error_code) +
        struct.pack('>i', api_keys_count) +
        api_entry
    )
    
    response_header = struct.pack('>i', correlation_id)
    
    message_length = 20
    response_message_length = struct.pack('>i', message_length)
    
    response = response_message_length + response_header + response_body
    
    conn.sendall(response)
    conn.close()

if __name__ == "__main__":
    main()