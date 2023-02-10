from typing import BinaryIO

class StreamWriter:
    def __init__(self, file: BinaryIO) -> None:
        self.file = file

    def send(self, message: bytes, *, flush: bool = True) -> None:
        self.file.write(message)
        self.file.write(b"\0")

        if flush:
            self.file.flush()
