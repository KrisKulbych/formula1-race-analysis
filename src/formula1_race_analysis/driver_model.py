from dataclasses import dataclass


@dataclass(order=True)
class Driver:
    id: str
    name: str
    car_model: str
