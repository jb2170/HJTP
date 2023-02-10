import json

from ..NullTerminatedBytes.StreamReader import StreamReader as NullTerminatedBytesStreamReader

class StreamReader(NullTerminatedBytesStreamReader):
    def __next__(self):
        message = super().__next__()
        return json.loads(message[:-1])
