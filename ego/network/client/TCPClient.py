from typing import Union

from time import sleep
from socket import socket
from socket import AF_INET, SOCK_STREAM

from ego.logger.service.LoggerCoreService import LoggerCoreService

log = LoggerCoreService.get_logger_instance()


class TCPClient:
    # NULL
    NULL_FLAG = bytes().fromhex("00")
    # ETX
    ETX_FLAG = bytes().fromhex("03")
    # EOT
    EOT_FLAG = bytes().fromhex("04")

    def __init__(self, host, port, rx_buf_len=512, tx_buf_len=512, blocking=True):
        self.host = host
        self.port = port
        self.rx_buf_len = rx_buf_len
        self.tx_buf_len = tx_buf_len
        self.blocking = blocking
        self.buffer = None
        self.data = ""
        self.send_flag = False
        self.rec_flag = False
        self.client: socket | None = None

    def set_blocking(self, blocking):
        self.blocking = blocking
        if self.client:
            self.client.setblocking(blocking)

    def connect(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.client.setblocking(self.blocking)

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            log.exception(e)

    def tx(self, data: Union[str, bytes] = None, data_size=0) -> None:
        """
            Example for tx
        """
        send_timeout = 5
        tx_len_count = 0

        if type(data) == str:
            pre_data = data.encode("UTF-8")
        else:
            pre_data = data
        # 添加结束符
        pre_data += self.EOT_FLAG

        if data_size > 0:
            length = data_size
        else:
            length = len(pre_data)

        while tx_len_count < length:
            tx_len = self.client.send(pre_data[tx_len_count:])
            if tx_len <= 0:
                log.warning("socket connection timeout, wait...")
                send_timeout = send_timeout - 1
                sleep(1)
                if send_timeout == 0:
                    raise RuntimeError("socket connection broken")
                continue

            tx_len_count = tx_len_count + tx_len

    def rx(self) -> bytes:
        """
            Example for rx
        """
        data = b""
        while True:
            try:
                chunk = self.client.recv(self.rx_buf_len)
                if not chunk:
                    return data
                data += chunk

                if self.EOT_FLAG in data:
                    eot_index = data.index(self.EOT_FLAG)
                    return data[:eot_index]
            except Exception as e:
                log.debug("没收到消息了。")
                log.exception(e)
                return data


if __name__ == "__main__":
    client = TCPClient("localhost", 2334, rx_buf_len=512, tx_buf_len=512)
    client.connect()

    # while True:
    #     msg = input()
    #     if not msg or msg == "EOF" or msg.find('\\n') != -1 or msg.find('\\r') != -1 :
    #         print("enter")
    #         break

    # msg = """
    # {
    #     "file_name": "catalina.out"
    # }
    # """
    # client.tx(msg)
    # client.rx()
