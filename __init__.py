import samp
from pysamp import *
from pysamp.player import Player
from python.dialogchain import DialogChain


samp.config(encoding='cp1251')


@on_gamemode_init
def on_gamemode_init():
    set_game_mode_text('Dialog Chain')


def dc_1_response(player: Player, response: int, select_item: int, input_text: str, *args, **kwargs):
    dialog_chain: DialogChain = kwargs['dialog_chain']
    current_dialog_id = dialog_chain.get_current_dialog_id()

    match current_dialog_id:
        case 0:
            if not response:
                player.send_client_message(-1, '{ff90aa}Thanks for watching demo DialogChain! <3')
                return
            
            elif not input_text.strip():
                dialog_chain.add_replacements({'error_message': ', {ff90aa}please{ffffff}'})
                return dialog_chain.update(player)
            
            dialog_chain.add_replacements({'input_text_from_dialog_0': input_text})
            return dialog_chain.next(player)
        
        case 1:
            if not response:
                dialog_chain.set_replacements({'error_message': ''})
                return dialog_chain.prev(player)
            
            match select_item:
                case 0:
                    return dialog_chain.show(player, 3)
                
                case _:
                    dialog_chain.add_replacements({'select_item_text': input_text})
                    return dialog_chain.next(player)
        
        case 2:
            return dialog_chain.prev(player)
                
        case 3:
            if not response:
                return dialog_chain.show(player, 1)
            
            dialog_chain.set_replacements({'error_message': ''})
            return dialog_chain.show(player)


dc_1_dialogs = [
    {
        'type': 1,
        'title': '{ffffaa}Dialog 0',
        'content': '{ffffff}Enter your name$error_message$:',
        'button_1': 'Next',
        'button_2': 'Close',
        'on_response': dc_1_response,
        'custom_arg_1': 1,
        'custom_arg_2': 2
    },
    {
        'type': 2,
        'title': '{ffffaa}Dialog 1',
        'content': '{ffffff}Your name: {90ffaa}$input_text_from_dialog_0$\nList item 2\nList item 3',
        'button_1': 'Select',
        'button_2': 'Back',
        'on_response': dc_1_response
    },
    {
        'type': 0,
        'title': '{ffffaa}Dialog 2',
        'content': '{ffffff}You select: {90ffaa}$select_item_text$',
        'button_1': 'Cool',
        'button_2': '',
        'on_response': dc_1_response
    },
    {
        'type': 0,
        'title': '{ffffaa}Dialog 3',
        'content': '{ffffff}Want to change your name?',
        'button_1': '{ffffaa}Yes',
        'button_2': 'No, thx',
        'on_response': dc_1_response
    }
]


@Player.on_connect
def on_player_connect(player: Player):
    dc_1 = DialogChain.create(dc_1_dialogs)
    dc_1.add_replacements({'error_message': ''})
    dc_1.show(player)
