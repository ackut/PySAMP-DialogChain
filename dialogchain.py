from pysamp.dialog import Dialog
from pysamp.player import Player


class DialogChain:
    def __init__(self, dialogs: list) -> None:
        self.current_dialog_id: int
        self.dialogs: list[dict] = dialogs
        self.storage: dict = {}
        self.replacements: dict = {}

    @classmethod
    def create(cls, dialogs: list) -> "DialogChain":
        return cls(dialogs)
    
    def set_current_dialog_id(self, dialog_id: int) -> int:
        self.current_dialog_id = dialog_id
        return dialog_id
    
    def get_current_dialog_id(self) -> int:
        return self.current_dialog_id
    
    def set_storage(self, storage: dict) -> dict:
        self.storage = storage
        return self.storage
    
    def add_to_storage(self, data: dict) -> dict:
        self.storage.update(data)
        return self.replacements

    def get_storage(self) -> dict:
        return self.storage
    
    def set_replacements(self, replacements: dict) -> dict:
        self.replacements = replacements
        return self.replacements
    
    def add_replacements(self, replacements: dict) -> dict:
        self.replacements.update(replacements)
        return self.replacements

    def get_replacements(self) -> dict:
        return self.replacements
    
    def show(self, player: "Player", dialog_id: int = 0) -> int:
        self.set_current_dialog_id(dialog_id)
        dialog_data = self.dialogs[dialog_id].copy()

        if self.get_replacements():
            for k, v in self.get_replacements().items():
                dialog_data['content'] = str.replace(
                    dialog_data['content'], f'${k}$', v
                )
        
        Dialog.create(*dialog_data.values(), dialog_chain=self).show(player)
        return dialog_id
    
    def next(self, player: "Player") -> int:
        if self.current_dialog_id < len(self.dialogs) - 1:
            return self.show(player, self.current_dialog_id + 1)
        
        return self.show(player, self.current_dialog_id)
        
    def prev(self, player: "Player") -> int:
        if self.current_dialog_id > 0:
            return self.show(player, self.current_dialog_id - 1)
        
        return self.show(player)
    
    def update(self, player: "Player") -> int:
        return self.show(player, self.get_current_dialog_id())
    