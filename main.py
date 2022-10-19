from typing import Dict, Iterable, cast

from memory import Memory
from storage import AddressData, TankData, TankDataCSV, TankDataStorage
from structure import ClassFactory, Struct


class UnitSettings:
    def __init__(self, mem: Memory, settings: Struct):
        self.__mem = mem
        self.__settings = settings

    def set(self, path: Iterable[str], value: float) -> None:
        if value == -1:
            return
        self.__mem.write_float(self.__settings.find(*path), value)

    def get(self, path: Iterable[str]) -> float:
        return self.__mem.read_float(self.__settings.find(*path))


PROCESS_NAME = "TankForce.exe"
TANKS_DATA_PATH = "data.csv"
TANKS_ADDRESS_PATH = "addresses.txt"

memory = Memory(PROCESS_NAME)
factory = ClassFactory()
tanks_data: TankDataStorage = TankDataCSV(TANKS_DATA_PATH)
unit_addr_data = AddressData("addresses.txt")

tank_map: Dict[int, TankData] = {}
for data in tanks_data.load():
    tank_map[data.id] = data

def hack(unit_addr: int)->None:
    unit = factory.make_unit()
    memory.set_addr(unit, unit_addr)

    unit_id = memory.read_int(unit)
    # WARNING: handle case when the ID of unit is not in database
    # if unit_id not in tank_map:
    #     continue
    data = tank_map[unit_id]
    sync(unit, data)


def sync(unit: Struct, data: TankData) -> None:
    settings = cast(Struct, unit["settings"])
    unit_settings = UnitSettings(memory, settings)

    unit_settings.set(("hp", "current"), data.hp)
    unit_settings.set(("hp", "max"), data.hp)
    unit_settings.set(("speed", "current"), data.speed)
    unit_settings.set(("speed", "max"), data.speed)
    unit_settings.set(("turet", "current"), data.turet)
    unit_settings.set(("turet", "max"), data.turet)
    unit_settings.set(("acceleration", "current"), data.acceleration - 2)
    unit_settings.set(("acceleration", "current"), data.acceleration)
    unit_settings.set(("acceleration", "max"), data.acceleration)
    unit_settings.set(("turn", "current"), data.turn)
    unit_settings.set(("turn", "max"), data.turn)
    unit_settings.set(("reload", "current"), data.reload)
    unit_settings.set(("reload", "max"), data.reload)
    # TODO: set damage
    # unit_settings.set(("damage", "min"), 0)


for unit_addr in unit_addr_data.load():
    hack(unit_addr)
