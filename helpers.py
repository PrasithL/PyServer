import mimetypes
import os
import socket
import typing
import config
import http_responses as http


def iter_lines(sock: socket.socket, bufsize: int = 16384) -> typing.Generator[bytes, None, bytes]:
    """
    Given a socket, read all the individual CRLF-separated lines
    and yield each one until an empty one is found.  Returns the
    remainder after the empty line.
    """

    buff = b""

    while True:
        data = sock.recv(bufsize)
        if not data:
            return b""

        buff += data

        while True:
            try:
                i = buff.index(b"\r\n")
                line, buff = buff[:i], buff[i + 2:]
                if not line:
                    return buff

                yield line
            except IndexError:
                break


def serve_file(sock: socket.socket, path: str) -> None:
    """Given a socket and the relative path to a file (relative to
    SERVER_SOCK), send that file to the socket if it exists.  If the
    file doesn't exist, send a "404 Not Found" response.
    """
    if path == "/":
        path = "/index.html"

    abspath = os.path.normpath(os.path.join(os.path.abspath(config.SERVER_ROOT), path.lstrip("/")))
    print(abspath)
    if not abspath.startswith(os.path.abspath(config.SERVER_ROOT)):
        sock.sendall(http.NOT_FOUND_RESPONSE)
        return

    try:
        with open(abspath, "rb") as f:
            stat = os.fstat(f.fileno())
            content_type, encoding = mimetypes.guess_type(abspath)
            if content_type is None:
                content_type = "application/octet-stream"

            if encoding is not None:
                content_type += "; charset=" + encoding

            response_headers = http.FILE_RESPONSE_TEMPLATE.format(
                content_type=content_type,
                content_length=stat.st_size,
            ).encode("ascii")

            sock.sendall(response_headers)
            sock.sendfile(f)
    except FileNotFoundError:
        sock.sendall(http.NOT_FOUND_RESPONSE)
        return
