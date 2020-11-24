import socket
import threading
import pickle


class Client:
    def __init__(self, host="localhost", port=4000):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))

        msg_recv = threading.Thread(target=self.recvData)
        msg_recv.daemon = True
        msg_recv.start()
        
        self.state =  {
            # 'player_body': [],
            # 'opponent': []
        }

    def recvData(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    self.state = pickle.loads(data)
            except:
                pass

    def sendStatus(self):
        self.sock.send(pickle.dumps(self.state))

    def close(self):
        self.sock.close()

