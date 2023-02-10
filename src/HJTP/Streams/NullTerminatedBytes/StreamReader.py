from typing import BinaryIO, List, Optional
import os

class StreamReader:
    def __init__(self, file: BinaryIO, *, limit: Optional[int] = None) -> None:
        self.file = file
        self.limit = limit # TODO NotImplemented

        self.ongoing_message = bytes()
        self.messages: List[bytes] = []

    def __iter__(self):
        return self

    def __next__(self) -> bytes:
        while True:
            if self.messages:
                return self.messages.pop(0)

            if not (chunk := os.read(self.file.fileno(), 4096)):
                # we discard non-null-terminated self.ongoing_message_chunk
                raise StopIteration

            self.ongoing_message += chunk

            while True:
                try:
                    message_terminator_index = self.ongoing_message.index(b"\0")
                except ValueError:
                    break

                self.messages.append(self.ongoing_message[:message_terminator_index + 1])
                self.ongoing_message = self.ongoing_message[message_terminator_index + 1:]
