import socketserver

from .StreamReader import StreamReader
from .StreamWriter import StreamWriter

class StreamRequestHandler(socketserver.StreamRequestHandler):
    def setup(self) -> None:
        super().setup()
        self.rstream = StreamReader(self.rfile)
        self.wstream = StreamWriter(self.wfile)
