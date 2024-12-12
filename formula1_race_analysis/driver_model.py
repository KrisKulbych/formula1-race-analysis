from dataclasses import dataclass, field


@dataclass(order=True)
class Driver:
    driver_id: str
    driver_name: str
    car_model: str
    start_time: str | None = field(default=None, init=False, compare=False)
    end_time: str | None = field(default=None, init=False, compare=False)
    race_duration: float = field(default_factory=float, init=False, compare=True)
    q1_position: int = field(default_factory=int, init=False, compare=True)

    def __iter__(self) -> tuple[str, str, str, float, int]:
        return (self.driver_id, self.driver_name, self.car_model, self.race_duration, self.q1_position)
