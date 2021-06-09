import socket
import sqlite3
import datetime

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('127.0.0.1', 54322))
    print('server is listening at {} : {}'.format(*s.getsockname()))

    with sqlite3.connect('data.sqlite3') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS station_status (
               station_id INT,
               last_date TEXT,
               alarm1 INT,
               alarm2 INT,
               PRIMARY KEY(station_id)
               );''')

        while True:
            data, addr = s.recvfrom(1024)
            data = data.decode()
            print('IP: {}, PORT: {},data is: {}'.format(addr[0], addr[1], data))
            word = data.split()

            try:
                if len(word) != 3:
                    raise IndexError
                station_id = int(word[0])
                alarm1 = int(word[1])
                alarm2 = int(word[2])
                last_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                print('''Data to DB: [station_id:{}], [alarm1:{}],[alarm2:{}], [last_date:{}] '''
                      .format(station_id, alarm1, alarm2, last_date))
                conn.execute(
                    'INSERT OR REPLACE INTO station_status VALUES (?, ?, ?, ?)',
                    (station_id, last_date, alarm1, alarm2)
                )
                conn.commit()
                message_send="Ok"
            except ValueError:
                message_send="The values are not Integer, please correct them."
                print(message_send)
            except IndexError:
                message_send = "There are not exactly 3 arguments, please correct them."
                print(message_send)
            s.sendto(message_send.encode(), addr)


