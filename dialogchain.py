from typing import Callable, Optional
from pysamp.dialog import Dialog
from pysamp.player import Player


class DialogChain:
    def __init__(
        self,
        player: "Player",
        dialogs: list,
        title: str,
        on_response: Optional[Callable]
    ) -> None:
        self.player: "Player" = player
        self.last_dialog_id: int = 0
        self.current_dialog_id: int = 0
        self.title: str = title
        self.on_response: Optional[Callable] = on_response
        self.dialogs: list[dict] = dialogs
        self.storage: dict = {}
        self.placeholders: dict = {}

    @classmethod
    def create(
        cls,
        for_player: "Player",
        dialogs: list,
        title: str = None,
        on_response: Optional[Callable] = None
    ) -> "DialogChain":
        return cls(for_player, dialogs, title, on_response)
    
    def set_current_dialog_id(self, dialog_id: int) -> int:
        self.current_dialog_id = dialog_id
        return dialog_id
    
    def get_current_dialog_id(self) -> int:
        return self.current_dialog_id
    
    def set_last_dialog_id(self, dialog_id: int) -> int:
        self.last_dialog_id = dialog_id
        return dialog_id
    
    def get_last_dialog_id(self) -> int:
        return self.last_dialog_id
    
    def set_storage(self, storage: dict) -> dict:
        self.storage = storage
        return self.storage
    
    def add_to_storage(self, data: dict) -> dict:
        self.storage.update(data)
        return self.placeholders

    def get_storage(self) -> dict:
        return self.storage
    
    def set_placeholders(self, placeholders: dict) -> dict:
        self.placeholders = placeholders
        return self.placeholders
    
    def add_placeholders(self, placeholders: dict) -> dict:
        self.placeholders.update(placeholders)
        return self.placeholders

    def get_placeholders(self) -> dict:
        return self.placeholders
    
    def show(self, dialog_id: int = 0) -> int:
        """ Open dialog from dialog list """
        if dialog_id != self.get_current_dialog_id():
            self.set_last_dialog_id(self.get_current_dialog_id())
            self.set_current_dialog_id(dialog_id)

        storage = self.get_storage()
        placeholders = self.get_placeholders()
        dialog = self.dialogs[dialog_id].copy()
        dialog_title = dialog['title'] if 'title' in dialog else self.title

        for k, v in storage.items():
            self.add_placeholders({f's:{k}': v})

        if placeholders or storage:
            for k, v in placeholders.items():
                dialog['content'] = str.replace(
                    dialog['content'], f'${k}$', str(v)
                )
                dialog_title = str.replace(
                    dialog_title, f'${k}$', str(v)
                )
        
        Dialog.create(
            type=dialog['type'],
            title=dialog_title,
            content=dialog['content'],
            button_1=dialog['buttons'][0],
            button_2=dialog['buttons'][1],
            on_response=dialog['on_response'] if 'on_response' in dialog else self.on_response,
            *[i for i in dialog.values()][6:],
            dialog_chain=self
        ).show(self.player)
        
        return dialog_id
    
    def next(self) -> int:
        """ Open next dialog from dialog list """
        if self.current_dialog_id < len(self.dialogs) - 1:
            return self.show(self.current_dialog_id + 1)
        
        return self.show(self.current_dialog_id)

    def prev(self) -> int:
        """ Open previous dialog from dialog list """
        if self.current_dialog_id > 0:
            return self.show(self.current_dialog_id - 1)

        return self.show()
        
    def back(self) -> int:
        """ Open last closed dialog from this DialogChain """
        return self.show(self.get_last_dialog_id())
    
    def update(self) -> int:
        """ Reopen current DialogChain dialog """
        return self.show(self.get_current_dialog_id())
    