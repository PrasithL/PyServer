
SUCCESS_RESPONSE = b"""
HTTP/1.1 200 OK
Content-type: text/html
Content-length: 15

<h1>OK</h1>
""".replace(b"\n", b"\r\n")

BAD_REQUEST_RESPONSE = b"""
HTTP/1.1 400 Bad Request
Content-type: text/plain
content-length: 11

Bad Request""".replace(b"\n", b"\r\n")

NOT_FOUND_RESPONSE = b"""
HTTP/1.1 400 Not Found
Content-type: text/plain
Content-length: 9

Not Found""".replace(b"\n", b"\r\n")

METHOD_NOT_ALLOWED_RESPONSE = b"""\
HTTP/1.1 405 Method Not Allowed
Content-type: text/plain
Content-length: 17

Method Not Allowed""".replace(b"\n", b"\r\n")

FILE_RESPONSE_TEMPLATE = """\
HTTP/1.1 200 OK
Content-type: {content_type}
Content-length: {content_length}

""".replace("\n", "\r\n")
