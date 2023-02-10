#!/usr/bin/env python3

import json

import socketserver

from HJTP.Streams.NullTerminatedJSON.StreamRequestHandler import StreamRequestHandler
from HJTP.Server.ResponseException import ResponseException

class Handler(StreamRequestHandler):
    def handle_single_message(self, message) -> None:
        key = "method"

        if key not in message:
            raise ResponseException(400, f"{repr(key)} not in request")

        method: str = message[key]

        if not isinstance(method, str):
            raise ResponseException(400, "Invalid method")

        if method != "get":
            raise ResponseException(501, f"Method {repr(method)} not implemented")

        key = "filename"

        if key not in message:
            raise ResponseException(400, f"{repr(key)} not in request")

        filename: str = message[key]

        if not isinstance(filename, str):
            raise ResponseException(400, "Invalid filename")

        try:
            with open(filename, "rb") as f:
                file_bytes = f.read().hex()
        except (FileNotFoundError, NotADirectoryError, IsADirectoryError):
            raise ResponseException(404, f"{repr(filename)}: {FileNotFoundError.__name__}")
        except PermissionError:
            raise ResponseException(403, f"{repr(filename)}: {PermissionError.__name__}")

        self.wstream.send({
            "code": 200,
            "body": file_bytes
        })

    def handle(self) -> None:
        while True:
            try:
                message = next(self.rstream)
            except StopIteration:
                break
            except json.JSONDecodeError:
                self.wstream.send({
                    "code": 400,
                    "error-message": "Invalid request"
                })
                continue

            try:
                self.handle_single_message(message)
            except ResponseException as e:
                self.wstream.send({
                    "code": e.code,
                    "error-message": e.message
                })
                continue
            except Exception:
                self.wstream.send({
                    "code": 500,
                    "error-message": "An internal server error occurred"
                })
                raise

ADDRESS = ("127.0.0.1", 8080) # TODO copy argparse stuff from SocketCat

def main() -> None:
    with socketserver.ForkingTCPServer(ADDRESS, Handler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt as e:
            print(f"{e.__class__.__name__}: shutting down")

if __name__ == "__main__":
    main()
