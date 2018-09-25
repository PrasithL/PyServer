import socket
from typing import NamedTuple
import helpers


class Request():
    method = ""
    path = ""
    headers = {}

    def __init__(self, method, path, headers):
        self.method = method
        self.path = path
        self.headers = headers

    @classmethod
    def from_socket(cls, sock: socket.socket) -> "Request":
        """Read and parse the request from a socket object.

        Raises:
          ValueError: When the request cannot be parsed.
        """

        lines = helpers.iter_lines(sock)

        try:
            request_line = next(lines).decode("ascii")
        except StopIteration:
            raise ValueError("Request line missing")

        try:
            method, path, _ = request_line.split(" ")
        except ValueError:
            raise ValueError("Malformed request line " + request_line)

        headers = {}
        for line in lines:
            try:
                name, _, value = line.decode("ascii").partition(":")
                headers[name.lower()] = value.lstrip()
            except ValueError:
                raise ValueError("Malformed request line " + line)

        return cls(method, path, headers)
