import socket
import struct

def encode_varint(value: int) -> bytes:
    return value.to_bytes(1, byteorder='big')

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
    first_response = struct.unpack('>h', data[offset:offset + 2])[0]
    offset += 2

    second_response = struct.unpack('>h', data[offset:offset + 2])[0]
    offset += 2

    correlation_id = struct.unpack('>i', data[offset:offset + 4])[0]

    response_header = struct.pack('>i', correlation_id)
    
    throttle_time_ms = struct.pack('>i', 0)
    
    error_code = struct.pack('>h', 0)
    api_keys_array_length = encode_varint(2)
    api_entry = struct.pack('>hhh', 18, 0, 4) + encode_varint(0)
    
    body_tagged_fields = encode_varint(0)
    
    response_body = throttle_time_ms + error_code + api_keys_array_length + api_entry + body_tagged_fields
    
    message_length = 4 + len(response_body)
    response_message_length = struct.pack('>i', message_length)
    
    response = response_message_length + response_header + response_body

    conn.sendall(response)
    conn.close()

if __name__ == "__main__":
    main()
