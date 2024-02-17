# DialogChain - simplify dialog system.

## Features
1. Easy to work with dialogs. DRY.
2. Replaceable placeholders: `$placeholder_value$`.
3. Storage in the dialog chain. (And also custom placeholders: `%storage_value%`)
4. Easy navigation through the chain: `.show(dialog_id) .next() .back() .update()`
5. Return to last closed dialog: `.back()`

### Setup
1. Add *args, **kwargs to your ./python/pysamp/dialog.py (For example from this repository).
2. Put dialogchain.py from this repository from your ./python/ folder.

### Use
Check `__init__.py` from repo, for more information.

1. Import DialogChain class from dialogchain.py
2. Create dialog chain response function, using template:
```py
dc_1_response(player: Player, response: int, select_item: int, input_text: str, *args, **kwargs):
     dc: DialogChain = kwargs['dialog_chain']

     match dc.get_current_dialog_id():
          case 0:
               if not response:
                    return dc.update()
     
               return dc.next()
     
          case _:
               if not response:
                    return dc.back()
          
               return dc.update()
```
3. Create dialog list using template:
```py
dc_1_dialogs: list[dict] = [
     {
          'type': 0,
          'content': 'Content in dialog 0',
          'buttons': ['Next', 'Back']
     },
     {
          'type': 0,
          'content': 'Content in dialog 1',
          'buttons': ['', 'Back']
     }
]
```
5. Create and show dialog chain, using DialogChain.create() method.
```py
DialogChain.create(
     for_player=player,
     dialogs=dc_1_dialogs,
     title='Default Title'
     on_response=dc_1_response
).show()
```
