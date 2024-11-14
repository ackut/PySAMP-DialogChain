import re
from enum import Enum
from typing import Annotated, Optional, Callable, Dict
from pydantic import BaseModel, Field, field_validator
from pydantic.functional_validators import AfterValidator

from samp import ShowPlayerDialog  # type: ignore
from pysamp.event import registry


# def remove_colors_from_text(text: str) -> str:
#     return re.sub(r"{[A-Fa-f0-9]{6}}", "", text)


# def check_text_length(text: str, min_length: int, max_length: int) -> bool:
#     return min_length <= len(text) <= max_length


class DialogStyle(Enum):
    MSGBOX = 0
    INPUT = 1
    LIST = 2
    PASSWORD = 3
    TABLIST = 4
    TABLIST_HEADERS = 5


# TODO: validate without colors.
class DialogSchema(BaseModel):
    style: DialogStyle
    title: str = Field(max_length=32)
    content: str = Field(max_length=2048)
    button_1: str = Field(max_length=8)
    button_2: Optional[str] = Field("", max_length=8)
    handler: Optional[Callable] = None


class DialogResponseSchema(BaseModel):
    player_id: int
    response: bool
    list_item: Optional[int] = None
    input_text: Optional[str] = None


class Dialog:
    _ID: int = 32767  # random dialog identifier to be used in SA-MP.
    _registry: Dict[int, "Dialog"] = {}

    def __init__(self, schema: DialogSchema, *args, **kwargs) -> None:
        self._style = schema.style.value
        self._title = schema.title
        self._content = schema.content
        self._button_1 = schema.button_1
        self._button_2 = schema.button_2
        self._handler = schema.handler
        self._args = args
        self._kwargs = kwargs

    @classmethod
    def create(cls, schema: DialogSchema, *args, **kwargs) -> "Dialog":
        return cls(schema, *args, **kwargs)

    def show(self, player_id: int) -> bool:
        if ShowPlayerDialog(
            player_id,
            Dialog._ID,  # we only occupy one ID on SA-MP side.
            self._style,
            self._title,
            self._content,
            self._button_1,
            self._button_2,
        ):
            Dialog._registry[player_id] = self
            return True
        return False

    @classmethod
    def hide(cls, player_id: int) -> bool:
        if ShowPlayerDialog(player_id, -1, 0, "", "", "", ""):
            cls._registry.pop(player_id, None)
            return True
        return False

    @classmethod
    def handle(
        cls,
        player_id: int,
        dialog_id: int,
        response: int,
        list_item: int,
        input_text: str,
    ) -> Optional[Callable]:
        instance = cls._registry.get(player_id)

        if dialog_id == cls._ID and instance and instance._handler:
            return instance._handler(
                player_id,
                response,
                list_item,
                input_text,
                *instance._args,
                **instance._kwargs,
            )
        return None

    @property
    def style(self) -> str:
        return self._style

    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def button_1(self) -> str:
        return self._button_1

    @property
    def button_2(self) -> str:
        return self._button_2

    @property
    def handler(self) -> Optional[Callable]:
        return self._handler


registry.register_callback(
    'OnDialogResponse',
    Dialog.handle,
    'dialogchain.dialogs',
)
