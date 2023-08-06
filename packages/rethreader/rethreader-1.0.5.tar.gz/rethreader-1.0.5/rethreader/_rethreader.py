import sys
import threading
from collections import namedtuple
from time import sleep
from typing import Optional, Iterable, List, Set

_Key = namedtuple("Key", ["id", "target", "args", "kwargs"])


class Description(str):
    def __init__(self, string: str):
        super().__init__()
        self.string = string
        self._null_key = _Key(None, None, None, None)

    def __eq__(self, other):
        if isinstance(other, Description):
            return self.string == other.string
        return False

    def __repr__(self):
        return f"Description('{self}')"


_no_result = Description("No Result")


class KeyThread(threading.Thread):
    def __init__(self, key: _Key, daemon: Optional[bool] = None):
        self.key = key
        n, target, args, kwargs = key
        if kwargs is None:
            kwargs = {}
        self.id = n
        self.killed = False
        self._result = _no_result
        super(KeyThread, self).__init__(target=(lambda t: self.set_result(t(*args, **kwargs))),
                                        args=(target,), daemon=daemon)
        self._run_backup = self.run

    def globaltrace(self, _, event, __):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, _, event, __):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
        if self.is_alive():
            self.join(0)
        return self

    @property
    def info(self):
        return '; '.join(str(i) for i in list(self.key)[1:])

    @classmethod
    def of(cls, target=None, args=(), kwargs=None, daemon=None):
        return cls(_Key(None, target, args, kwargs), daemon)

    @property
    def result(self):
        return self._result

    def run(self):
        super(KeyThread, self).run()
        return self

    def run_with_trace(self):
        sys.settrace(self.globaltrace)
        self._run_backup()
        self.run = self._run_backup

    def set_result(self, result):
        self._result = result

    def start(self):
        self.run = self.run_with_trace
        super(KeyThread, self).start()
        return self


def _is_unpacked(_object) -> bool:
    if isinstance(_object, _Key):
        return True
    return isinstance(_object, tuple) and len(_object) == 4 and isinstance(_object[0], (int, type(None))) and \
           callable(_object[1]) and isinstance(_object[2], tuple) and isinstance(_object[3], dict)


def _thread_info(self) -> str:
    if isinstance(self, KeyThread):
        return self.info
    elif _is_unpacked(self):
        _, a, b, c = self
        self = a, tuple(b), dict(c)
        return '; '.join(str(i) for i in self)


class Rethreader:
    def __init__(self, target=None, queue: Optional[Iterable] = None, max_threads: int = 16, clock_delay: float = 0.01,
                 auto_quit: Optional[bool] = None, save_results=True, daemon: bool = False):
        if target is not None:
            assert callable(target)
        self._target = target
        self._main: Set[KeyThread] = set()
        self._in_delay_queue: int = 0
        if save_results:
            self._finished: Set[KeyThread] = set()
        else:
            self._finished: int = 0
        self._daemonic: bool = daemon
        self._clock: float = clock_delay
        self._max_threads: int = 0 if max_threads < 0 else max_threads
        self._queue: List[_Key] = []
        if queue:
            [self.add(_t) for _t in queue]
        self._auto_quit: bool = auto_quit if auto_quit else bool(queue)
        self._running: bool = False
        self._start_thread = None

    def __add__(self, *args, **kwargs):
        self._append(self._unpack(*args, **kwargs))
        return self

    def __enter__(self):
        if not self._running:
            self.start()
        return self.auto_quit(False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._auto_quit = True

    def __len__(self) -> int:
        return self.remaining + self.finished

    def _unpack(self, *_object, **kwargs) -> _Key:
        if isinstance(_object, tuple) and len(_object) == 1:
            _object = _object[0]
        if _object and isinstance(_object, _Key):
            return _object
        target = None if self._target is None else self._target
        args = None
        _list = None
        if _object and isinstance(_object, Iterable) and not isinstance(_object, str):
            _list = list(_object)
            if not target and callable(_list[0]):
                target = _list.pop(0)
            if not kwargs:
                if _is_unpacked(_object):
                    _, target, args, kwargs = _object
                elif isinstance(_object, dict):
                    args, kwargs = (), _object
                elif _list:
                    if isinstance(_list[-1], dict):
                        kwargs = _list.pop(-1)
                else:
                    args = ()
        if target is not None:
            if args is None:
                if _list:
                    if len(_list) == 1 and isinstance(_list[0], tuple):
                        args = _list[0]
                    else:
                        args = tuple(_list)
                elif isinstance(_object, tuple):
                    args = _object
                else:
                    args = (_object,)
            return _Key(len(self), target, args, kwargs)
        return _Key(len(self), _object, (), kwargs)

    def _get_thread(self, target=None, args=(), kwargs=None) -> KeyThread:
        if isinstance(target, _Key):
            return KeyThread(target, self._daemonic)
        return KeyThread.of(target, args, kwargs, self._daemonic)

    def _load_target(self, target) -> KeyThread:
        if isinstance(target, KeyThread):
            return target
        return self._get_thread(self._unpack(target))

    def _start_next(self):
        next_target = self._queue.pop(0)
        next_thread = self._load_target(next_target)
        next_thread.start()
        self._main.add(next_thread)

    def run(self):
        _fin = isinstance(self._finished, set)
        self._running = True
        while self._running:
            for t in self._main.copy():
                if not t.is_alive():
                    if _fin:
                        self._finished.add(t)
                    else:
                        self._finished += 1
                    self._main.remove(t)
            while self._queue:
                if 0 < self._max_threads <= len(self._main):
                    break
                self._start_next()
            if self._auto_quit and self.is_empty():
                self._running = False
            else:
                sleep(self._clock)
        return self

    def _append(self, _object, _delay: int = 0):
        self._in_delay_queue += 1
        if _delay:
            sleep(_delay)
        self._queue.append(_object)
        self._in_delay_queue -= 1

    def _insert(self, _object, _index: int = 0):
        self._queue.insert(_index, _object)

    def add(self, *args, **kwargs):
        self._append(self._unpack(*args, **kwargs))
        return self

    def extend(self, _list: list):
        for i in _list:
            self.add(i)
        return self

    def insert(self, _index: int, *args, **kwargs):
        self._insert(self._unpack(*args, **kwargs), _index)
        return self

    def prioritize(self, _list: list):
        for i in reversed(_list):
            self._insert(self._unpack(i))
        return self

    def remove(self, *args, **kwargs):
        _object_thread = _thread_info(self._unpack(*args, **kwargs))
        for _list in (self._queue, self._main):
            for thread in _list.copy():
                if _thread_info(thread) == _object_thread:
                    if hasattr(thread, 'stop'):
                        thread.stop()
                    _list.remove(thread)
                    return self
        return self

    def postpone(self, delay, *args, **kwargs):
        _object = self._unpack(*args, **kwargs)
        self.remove(_object)
        self._get_thread(self._append, (_object, delay)).start()
        return self

    def auto_quit(self, _bool: bool = True):
        self._auto_quit = _bool
        return self

    @property
    def finished(self) -> int:
        if isinstance(self._finished, set):
            return len(self._finished)
        return self._finished

    @property
    def in_queue(self) -> int:
        return len(self._queue) + self._in_delay_queue

    def is_empty(self) -> bool:
        return self.remaining == 0

    def is_alive(self) -> bool:
        return self._running

    def kill(self):
        self._queue.clear()
        for thread in self._main:
            thread.kill()
        self._main.clear()
        self._running = False
        if self._start_thread:
            self._start_thread.kill()
        return self

    def quit(self):
        self.auto_quit()
        while self._running:
            sleep(self._clock)

    @property
    def remaining(self) -> int:
        return len(self._main) + self.in_queue

    @property
    def results(self) -> list:
        if isinstance(self._finished, set):
            return [None if i == _no_result else i.result
                    for i in sorted(self._finished, key=lambda x: x.id)]

    def start(self):
        self._start_thread = self._get_thread(self.run)
        self._start_thread.start()
        return self


if __name__ == '__main__':
    print("Hello world!")
