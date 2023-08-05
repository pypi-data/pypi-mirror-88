import threading

from six.moves.queue import Queue, Empty, Full
import socket
import sys
import errno

import rook.com_ws.socketpair_compat  # do not remove - adds socket.socketpair on Windows
from rook.com_ws import poll_select


MAX_QUEUE_SIZE = 2048
# this mustn't exceed the maximum socket buffer size allowed by the OS, so keep it small
SOCKET_SEMAPHORE_SIZE = 2 * MAX_QUEUE_SIZE


class SelectableQueue(object):
    """
    Uses a socketpair as a semaphore for reading and writing to the internal queue.
    This way, this queue can be used as a parameter to select() or poll().
    Maximum queue size is MAX_QUEUE_SIZE.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._queue = Queue(maxsize=MAX_QUEUE_SIZE)
        self._readsocket, self._writesocket = socket.socketpair()
        self._readsocket.setblocking(False)
        self._writesocket.setblocking(False)
        self._readsocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, SOCKET_SEMAPHORE_SIZE)
        self._writesocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SOCKET_SEMAPHORE_SIZE)

    def __del__(self):
        self._readsocket.close()
        self._writesocket.close()

    def put(self, item):
        with self._lock:
            if self._queue.full():
                return
            try:
                # writing to the socket with the lock locked is only OK
                # because the socket is non-blocking (setblocking(False))
                self._writesocket.send(b'1')
            except socket.error as exc:
                # if the socket wasn't ready for writing, send will raise EAGAIN
                # 11 on Linux for EAGAIN but 10035 on Windows for WSAEWOULDBLOCK
                if exc.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                    # queue is effectively full, so just return
                    return
                raise sys.exc_info()
            self._queue.put_nowait(item)

    def get(self):
        try:
            self._readsocket.recv(1)
        except socket.error as exc:
            # if the socket wasn't ready for reading, recv will raise EAGAIN
            # 11 on Linux for EAGAIN but 10035 on Windows for WSAEWOULDBLOCK
            if exc.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise Empty()
            raise sys.exc_info()

        with self._lock:
            return self._queue.get_nowait()

    def fileno(self):
        return self._readsocket.fileno()

    def qsize(self):
        return self._queue.qsize()
