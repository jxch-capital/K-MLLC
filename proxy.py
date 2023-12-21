import socket
import socks


def enable(host="localhost", port=10808):
    socks.setdefaultproxy(socks.SOCKS5, "localhost", 10808)
    socket.socket = socks.socksocket
