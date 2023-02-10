import json

from ..NullTerminatedBytes.StreamWriter import StreamWriter as NullTerminatedBytesStreamWriter

class StreamWriter(NullTerminatedBytesStreamWriter):
    def send(self, message, *, flush: bool = True) -> None:
        message_bytes = json.dumps(message, indent = 2, ensure_ascii = False).encode("UTF-8") + b"\n"
        super().send(message_bytes, flush = flush)
