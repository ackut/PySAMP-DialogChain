# DialogChain - simplify dialog system.

## Setup
1. Add *args, **kwargs to your ./python/pysamp/dialog.py (For example from this repository).
2. Put dialogchain.py from this repository from your ./python/ folder.

## Use
1. Import DialogChain class from dialogchain.py
2. Create dialog chain response function, using template:
   ```py
   dc_1_response(player: Player, response: int, input_text: str, select_item: int, *args, **kwargs):
        dialog_chain: DialogChain = kwargs['dialog_chain']
        current_dialog_id: int = dialog_chain.get_current_dialog_id()
   
        print(f'Your custom arguments in dialog {current_dialog_id}: {args}'
   
        match current_dialog_id:
             case 0:
                  if not response:
                       return dialog_chain.update(player)
         
                  return dialog_chain.next(player)
      
             case _:
                  if not response:
                       return dialog_chain.prev(player)
            
                  return dialog_chain.update(player)
   ```
3. Create dialog list using template:
   ```py
   dc_1_dialogs: list[dict] = [
        {
             'type': 0,
             'title': 'Dialog 0',
             'content': 'Content in dialog 0',
             'button_1': 'Next',
             'button_2': 'Back',
             'on_response': dc_1_response,
             'custom_arg_1': 'I Love Donuts'
        },
        {
             'type': 0,
             'title': 'Dialog 1',
             'content': 'Content in dialog 1',
             'button_1': '',
             'button_2': 'Back',
             'on_response': dc_1_response
        }
   ]
   ```
5. Create and show dialog chain, using DialogChain.create() method.
   ```py
   DialogChain.create(dc_1_dialogs).show(player)
   ```
