import zmq
import pickle
import threading


class Client:
    def __init__(self, host='localhost', port=5555) -> None:
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.s_req = self.context.socket(zmq.REQ)
        self.s_req.setsockopt(zmq.RCVTIMEO, 50)
        self.s_sub = self.context.socket(zmq.SUB)

        self.s_req.connect(f'tcp://{self.host}:{self.port+1}')
        self.s_sub.connect(f'tcp://{self.host}:{self.port}')

        self.on_message = None
        self.stop = False

    def _recv(self):
        import time
        while not self.stop:
            try:
                topic, msg = self.s_sub.recv_multipart()
                msg = pickle.loads(msg)
                topic = topic.decode()
                if self.on_message:
                    self.on_message(self, topic, msg)
            except:
                time.sleep(0.1)

    def publish(self, topic, msg):
        topic = topic.encode() if isinstance(topic, str) else topic
        try:
            self.s_req.send_multipart([topic, pickle.dumps(msg)])
            self.s_req.recv()
        except Exception as e:
            self.s_req.close()
            self.s_req = self.context.socket(zmq.REQ)
            self.s_req.setsockopt(zmq.RCVTIMEO, 50)
            self.s_req.connect(f'tcp://{self.host}:{self.port+1}')
            raise e

    def subscribe(self, topic):
        topic = topic.encode() if isinstance(topic, str) else topic
        self.s_sub.setsockopt(zmq.SUBSCRIBE, topic)

    def unsubscribe(self, topic):
        topic = topic.encode() if isinstance(topic, str) else topic
        self.s_sub.setsockopt(zmq.UNSUBSCRIBE, topic)

    def loop_start(self):
        threading.Thread(target=self._recv).start()

    def loop_forever(self):
        self._recv()

    def close(self):
        self.stop = True
        self.s_sub.close()
        self.s_req.close()
        self.context.term()

class Broker:
    def __init__(self, port=5555) -> None:
        self.port = port
        self.stop = False
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")

        self.socket_r = self.context.socket(zmq.REP)
        self.socket_r.bind(f'tcp://*:{port+1}')

    def _start(self):
        while not self.stop:
            try:
                message = self.socket_r.recv_multipart()
                print(message)
                self.socket_r.send_string('ok')
                self.socket.send_multipart(message)
            except:
                pass
            
    def loop_start(self):
        threading.Thread(target=self._start).start()

    def loop_forever(self):
        self._start()

    def close(self):
        self.stop = True
        self.socket.close()
        self.socket_r.close()
        self.context.term()
