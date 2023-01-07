from copy import copy
from dataclasses import dataclass


class FactoredArray():
    @dataclass
    class Item:
        val: any
        length: int = 0

        def __len__(self) -> int:
            return self.length

    def __init__(self, val=None, length=0) -> None:
        if length > 0:
            self._items = (FactoredArray.Item(val, length),)
        else:
            self._items = ()
            assert (length == 0)

        self._length = length

    def __add__(self, rhs):
        res = FactoredArray()
        if len(self._items) == 0 or len(rhs._items) == 0 or \
                self._items[-1].val != rhs._items[0].val:
            res._items = self._items + rhs._items
        else:
            res._items = self._items
            res._items[-1].length += len(rhs._items[0])
            res._items += rhs._items[1:]

        res._length = self._length + rhs._length

        return res

    def __getitem__(self, key):
        unwrap = False
        if isinstance(key, int):
            if key < 0:
                key = len(self) + key
            if key < 0 or key > len(self):
                raise IndexError

            key = slice(key, key + 1)
            unwrap = True

        if key.start < 0:
            key.start = self._length - key.start
        if key.stop < 0:
            key.stop = self._length - key.stop
        assert (key.step in (1, None))

        offset = 0
        item_it = iter(self._items)

        res = FactoredArray()

        while offset < key.start:
            delta = key.start - offset

            try:
                item = next(item_it)
            except BaseException:
                return res

            offset += len(item)
            if len(item) <= delta:
                continue

            tail_len = len(item) - delta
            res._items += (FactoredArray.Item(item.val, tail_len),)
            res._length += tail_len
            break

        while offset < key.stop:
            try:
                item = next(item_it)
            except BaseException:
                return res

            res._items += (copy(item),)
            res._length += len(item)
            offset += len(item)

        if offset > key.stop:
            res._items[-1].length -= (offset - key.stop)

        return res if not unwrap else res._items[0].val

    def __len__(self):
        return self._length


class TaggedBytes():
    def __init__(self) -> None:
        self.buf = bytes()
        self.tags = []

    def __init__(self, val, tag) -> None:
        self.buf = val
        self.tags = [tag]

    def __add__(self, val):
        res = TaggedBytes()
        res.buf = self.buf + val.buf
        if len(self.tags) == 0 or len(val.tags) == 0 or self.tags[-1].tag != val.tags[0].tag:
            res.tags = self.tags + val.tags
        else:
            left_len = len(self) - len(self.tags[-1])
            right_len = len(val) - len(val.tags[0])

            return self[:left_len] + \
                TaggedBytes(self.val[left_len:] + val[:right_len], val.tags[0].tag) + \
                val[right_len:]

        return res

    def __getitem__(self, key):
        if isinstance(key, int):
            key = slice(key, key + 1)

        offset = 0
        tag_it = iter(self.tags)

        while offset < key.start:
            pass


class MissingData():
    def __init__(self, length) -> None:
        self.length = length

    def __len__(self) -> int:
        return self.length


class GapPipe():
    def __init__(self, out_file, gap_filler, blend_len) -> None:
        self.out_file = out_file
        self.gap_filler = gap_filler

        self.blend_len = blend_len
        self.hist_len = gap_filler.get_lookback_len()

        self.data_buf = bytes()
        self.filler_buf = bytes()
        self.hist_buffer = bytes()

        self.blend_coeff = 0

    def push(buf):
        pass
