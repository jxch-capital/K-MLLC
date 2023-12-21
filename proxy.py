import socket
import socks


def enable(host="localhost", port=10808):
    socks.setdefaultproxy(socks.SOCKS5, host, port)
    socket.socket = socks.socksocket
