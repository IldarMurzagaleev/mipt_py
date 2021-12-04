import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))

    def get(self, metric):
        request = "get " + metric + "\n"
        request = bytes(request,'UTF-8')
        try:
            self.sock.sendall(request)
        except socket.error as msg:
            raise ClientError(msg)
        data = self.sock.recv(4096).decode("utf8")
        result = {}
        rows = data.strip().split('\n')
        status = rows[0]
        rows = rows[1:]
        if status == 'ok':
          for row in rows:
            values = row.split(' ')
            if len(values) != 3:
              raise ClientError(['wrong answer'])
            metric, value, timestamp = values
            try:
              value = float(value)
              timestamp = int(timestamp)
            except ValueError:
              raise ClientError(['wrong answer'])
            if metric not in result:
              result[metric] = [(timestamp, value)]
            else:
              result[metric].append((timestamp, value))
        else:
          raise ClientError(['wrong command'])
        result = {k: sorted(v, key=lambda item: item[0]) for k, v in result.items()}
        return result

    def put(self, metric, value, timestamp=None):
        tsmp = timestamp or int(time.time())
        request = "put " + metric + " " + str(value) + " " + str(tsmp) + "\n"
        request = bytes(request,'UTF-8')
        try:
            self.sock.sendall(request)
        except socket.error as msg:
            raise ClientError(msg)
        data = self.sock.recv(4096).decode("utf8")
        status = data.strip().split('\n')[0]
        if status == 'error':
          raise ClientError(['wrong command'])


class ClientError(Exception):
  def __init__(self, msg):
    self.message = 'Failed to put message. Error code: ' + str(msg[0])
    # переопределяется конструктор встроенного класса `Exception()`
    super().__init__(self.message)