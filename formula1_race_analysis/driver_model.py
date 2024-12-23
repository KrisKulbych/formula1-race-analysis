from dataclasses import dataclass, field


@dataclass(order=True)
class Driver:
    id: str
    name: str
    car_model: str
