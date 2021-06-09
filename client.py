import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        try:
            f = open('status.txt')
        except IOError:
            print("There is no file 'status.txt', please create one.")

        else:
            station_ID = f.readline().strip()
            alarm1 = f.readline().strip()
            alarm2 = f.readline().strip()
            f.close()
            message = station_ID + " " + alarm1 + " " + alarm2
            s.sendto(message.encode(), ('127.0.0.1', 54322))
            print("The message sent: ", message)
        data, addr = s.recvfrom(1024)
        print("Response from server: ", data.decode())
        time.sleep(60)