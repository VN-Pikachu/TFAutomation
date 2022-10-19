from __future__ import annotations
from typing import cast

from pymem import Pymem
from pymem.process import module_from_name

from structure import Base, Struct


class Memory:
    def __init__(self, process_name: str):
        self.mem = Pymem(process_name)
        self.module = module_from_name(
            self.mem.process_handle, process_name
        ).lpBaseOfDll

    def set_addr(self, obj: Base, addr: int) -> None:
        obj.addr = addr
        if not isinstance(obj, Struct):
            return

        for child in cast(Struct, obj).values():
            for i in range(len(child.offsets) - 1):
                addr = self.mem.read_ulonglong(addr + child.offsets[i])
            addr += child.offsets[-1]

            if isinstance(child, Struct):
                addr = self.mem.read_ulonglong(addr)

            self.set_addr(child, addr)

    def read_float(self, obj: Base) -> float:
        return self.mem.read_float(obj)

    def write_float(self, obj: Base, value: float) -> None:
        self.mem.write_float(obj, value)

    def read_int(self, obj: Base) -> int:
        return self.mem.read_int(obj)

    def write_int(self, obj: Base, value: int) -> None:
        self.mem.write_int(obj, value)
