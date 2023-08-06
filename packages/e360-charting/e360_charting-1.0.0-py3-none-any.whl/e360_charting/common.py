import enum


class BaseEnum(enum.Enum):
    def __str__(self):
        return str(self.value)

    @classmethod
    def to_list(cls) -> list:
        return [*map(str, cls)]
