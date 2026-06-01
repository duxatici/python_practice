import enum
from dataclasses import dataclass
from abc import ABC, abstractmethod


_parsers: dict[MessageType, type[Parser]] = {}


def register(message_type: MessageType):
    def decorator(cls):
        _parsers[message_type] = cls

        return cls

    return decorator


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class Parser(ABC):
    @abstractmethod
    def parse(self, message: JsonMessage) -> ParsedMessage:
        pass


class ParserFactory:
    def parse(self, message: JsonMessage) -> ParsedMessage:
        parser = _parsers[message.message_type]()

        parsed_message = parser.parse(message)

        return parsed_message


@register(MessageType.TELEGRAM)
class TelegramParser(Parser):
    def parse(self, message: JsonMessage) -> ParsedMessage: ...


@register(MessageType.MATTERMOST)
class MattermostParser(Parser):
    def parse(self, message: JsonMessage) -> ParsedMessage: ...


@register(MessageType.SLACK)
class SlackParser(Parser):
    def parse(self, message: JsonMessage) -> ParsedMessage: ...
