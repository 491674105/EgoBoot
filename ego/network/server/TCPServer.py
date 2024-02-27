from json import loads
from time import sleep

from socket import socket
from gevent.pool import Pool
from gevent import socket as g_socket

from ego import applicationContext

log = applicationContext.log


class TCPServer:
    exit_flag = '\036'

    def __init__(self, host, port, backlog=5, rx_buf_len=512, tx_buf_len=512, concurrent=5):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.rx_buf_len = rx_buf_len
        self.tx_buf_len = tx_buf_len
        self.buffer = None
        self.data = ""
        self.concurrent = concurrent
        self.pool = None
        self.service = None
        self.clients = {}

    def config(self, config_dict):
        for key in config_dict:
            if hasattr(self, key):
                setattr(self, key, config_dict[key])

    def run(self):
        log.info(f"server[{self.host}]:[{self.port}] ready to start...")
        self.service = socket()
        self.service.bind((self.host, self.port))
        self.service.listen(self.backlog)
        self.pool = Pool(self.concurrent)
        log.info(f"server[{self.host}]:[{self.port}] started!")

        while True:
            client, address = self.service.accept()
            self.clients[address] = client
            log.info(f"Client[{address}] is accessing...")
            self.pool.spawn(self.__handle_request, client)

    def __handle_request(self, client):
        while True:
            try:
                rx_buf = client.recv(self.rx_buf_len)
                if not rx_buf:
                    log.debug("等待连接...")
                    sleep(5)
                    continue
                self.buffer = rx_buf.decode(encoding='UTF-8')
                if self.buffer.find(self.exit_flag) != -1:
                    self.data = f"{self.data}{self.buffer.replace(self.exit_flag, '')}"
                    log.debug(f"receive: {self.data}")
                    param = loads(self.data)
                    if "signal" in param and param["signal"] == 200:
                        log.warn("服务器正在关闭...")
                        self.service.close()
                        log.warn("服务器已关闭")
                    file_path = f"E:\\documents\\{param['file_name']}"
                    with open(file_path, "rb") as file_byte:
                        self.transmit(client, msg=file_byte.read())
                else:
                    log.debug(f"buffer: {self.buffer}")
                    self.data = f"{self.data}{self.buffer}"
            except Exception as e:
                log.exception(e)
                client.shutdown(g_socket.SHUT_WR)
                break

    def transmit(self, client, msg=None):
        send_timeout = 5
        tx_len_count = 0
        self.data = f"{self.data}{self.exit_flag}"
        if msg:
            pre_data = msg
        else:
            pre_data = self.data.encode(encoding='UTF-8')
        length = len(pre_data)
        while tx_len_count < length:
            paragraph = pre_data[tx_len_count:]
            log.debug(paragraph.decode(encoding="UTF-8"))
            tx_len = client.send(paragraph)
            if tx_len == 0:
                log.warn("socket connection timeout, wait...")
                send_timeout = send_timeout - 1
                sleep(1)
                if send_timeout == 0:
                    raise RuntimeError("socket connection broken")
                continue

            tx_len_count = tx_len_count + tx_len
        self.data = ""


if __name__ == "__main__":
    print("start up this server...")
    server = TCPServer("0.0.0.0", 35001, rx_buf_len=512, tx_buf_len=512)
    server.run()
