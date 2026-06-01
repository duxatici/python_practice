from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str) -> None:
        self.path = path

    def __get__(self, instance: Model, owner: Model) -> JSON | None:
        if instance is None:
            return self

        value = instance.payload

        for key in self.path.split("."):
            if value is None:
                return None
            value = value.get(key)

        return value

    def __set__(self, instance: Model, value: str) -> None:
        current = instance.payload

        keys = self.path.split(".")

        for key in keys[:-1]:
            current = current[key]

        current[keys[-1]] = value
