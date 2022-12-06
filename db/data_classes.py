from dataclasses import dataclass


@dataclass
class Departments():
    id: int
    code: str
    name: str
    type_dep: str
    address: str
    coordinates: str
    days: str
    times: str

    def __init__(
            self, id: int, code: str,  name: str, type_dep: str, address: str,
            coordinates: str, days: str, times: str) -> None:

        self.id = id
        self.code = code
        self.name = name
        self.type_dep = type_dep
        self.address = address
        self.coordinates = coordinates
        self.days = days
        self.times = times
