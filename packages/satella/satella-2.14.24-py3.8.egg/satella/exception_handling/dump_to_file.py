from __future__ import print_function, absolute_import, division

import enum
import os
import typing as tp
import uuid

from satella.coding import silence_excs
from satella.files import DevNullFilelikeObject
from satella.instrumentation import Traceback
from .exception_handlers import BaseExceptionHandler

AsStreamTypeAccept = tp.Union[str, tp.IO, None]
AsStreamTypeAcceptHR = tp.Union[str, tp.TextIO]
AsStreamTypeAcceptIN = tp.Union[str, tp.BinaryIO]


class StreamType(enum.IntEnum):
    MODE_FILE = 0  # write to file
    MODE_STREAM = 1  # a file-like object was provided
    MODE_DEVNULL = 2  # just redirect to /dev/null


class AsStream:
    __slots__ = ('o', 'human_readable', 'mode', 'file')

    def __init__(self, o: AsStreamTypeAccept, human_readable: bool):
        """
        A stream to dump to

        :param o: stream, or a file name to use, or None to use /dev/null
        :param human_readable: whether the output should be human-readable
            or a pickle (False for pickle)
        """
        self.o = o
        self.human_readable = human_readable

        if isinstance(o, str):
            if os.path.isdir(o):
                self.o = os.path.join(o, uuid.uuid4().hex)

            self.mode = StreamType.MODE_FILE

        elif hasattr(o, 'write'):
            self.mode = StreamType.MODE_STREAM

        elif o is None:
            self.mode = StreamType.MODE_DEVNULL
        else:
            raise TypeError('invalid stream object')

    def __enter__(self) -> tp.Union[tp.TextIO, tp.BinaryIO]:
        if self.mode == StreamType.MODE_FILE:
            self.file = open(self.o, 'w' if self.human_readable else 'wb',
                             encoding='utf8' if self.human_readable else None)
            return self.file.__enter__()
        elif self.mode == StreamType.MODE_STREAM:
            return self.o
        elif self.mode == StreamType.MODE_DEVNULL:
            self.o = DevNullFilelikeObject()
            return self.o

    def __exit__(self, exc_type, exc_val, exc_tp):
        if self.mode == StreamType.MODE_FILE:
            return self.file.__exit__(exc_type, exc_val, exc_tp)
        elif self.mode == StreamType.MODE_STREAM:
            with silence_excs(AttributeError):
                self.o.flush()
        elif self.mode == StreamType.MODE_DEVNULL:
            pass


class DumpToFileHandler(BaseExceptionHandler):
    """
    Write the stack trace to a stream-file.

    Note that your file-like objects you throw into that must support only .write() and optionally
    .flush()

    :param human_readables: iterable of either a file-like objects, or paths where
        human-readable files will be output
    :param trace_pickles: iterable of either a file-like objects, or paths where pickles with
        stack status will be output
    :raises TypeError: invalid stream
    """
    __slots__ = ('hr', 'tb')

    def __init__(self, human_readables: tp.Iterable[AsStreamTypeAcceptHR],
                 trace_pickles: tp.Iterable[AsStreamTypeAcceptIN] = None):
        super(DumpToFileHandler, self).__init__()
        self.hr = [AsStream(x, True)
                   if not isinstance(x, AsStream) else x
                   for x in human_readables]  # type: tp.List[AsStream]
        self.tb = [AsStream(x, False) if not isinstance(x, AsStream) else x for x in
                   trace_pickles or []]  # type: tp.List[AsStream]

    def handle_exception(self, type_, value, traceback) -> bool:
        try:
            tb = Traceback()
        except ValueError:
            return False  # no traceback, probably hit KeyboardInterrupt or SystemExit,
            # continue with it

        for q in self.hr:
            with q as f:
                f.write('Unhandled exception caught: \n')
                tb.pretty_print(output=f)

        for q in self.tb:
            with q as f:
                f.write(tb.pickle())
