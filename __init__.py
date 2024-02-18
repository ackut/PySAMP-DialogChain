import samp
from pysamp import on_gamemode_init, set_game_mode_text
from pysamp.player import Player
from python.dialogchain import DialogChain


samp.config(encoding='cp1251')


@on_gamemode_init
def on_init():
    set_game_mode_text('DialogChain Demo')


def dc_demo_response(player: Player, response: int, select_item: int, input_text: str, *args, **kwargs):
    dc: DialogChain = kwargs['dialog_chain']
    dc_storage: dict = dc.get_storage()

    match dc.get_current_dialog_id():
        case 0:
            if not response:
                player.send_client_message(-1, '{90ffaa}Thanks for watching demo DialogChain! <3')
                return
            
            if not input_text.strip():
                dc.add_placeholders({'error_message': ', {ffaa90}please{ffffff}'})
                return dc.update()

            dc.add_to_storage({'player_name': input_text.strip()})
            return dc.next()

        case 1:
            if not response:
                return dc.show()
            
            dc.add_placeholders({'select_item_text': input_text.strip()})

            match select_item:
                case 0:
                    return dc.show(3)
                
                case 1:
                    dc_storage['click_counter'] += 1
                    return dc.update()
                
                case _:
                    return dc.next()
        
        case 3:
            if not response:
                return dc.back()
            
            dc.add_placeholders({'error_message': ''})
            return dc.show()
        

def custom_response(player: Player, response: int, select_item: int, input_text: str, *args, **kwargs):
    dc: DialogChain = kwargs['dialog_chain']
    return dc.back()


dc_demo_dialogs = [
    {
        'type': 1,
        'content': '{ffffff}Type your name$error_message$:',
        'buttons': ['Next', 'Close']
    },
    {
        'type': 2,
        'content': '{ffffff}Your name: {90ffaa}$player_name$\nClick counter: {90aaff}$click_counter$\nList item 2\nList item 3',
        'buttons': ['Select', 'Back']
    },
    {
        'type': 0,
        'title': '{ffaa90}Custom Title',
        'content': '{ffffff}You select: {90ffaa}$select_item_text$',
        'buttons': ['Cool', ''],
        'on_response': custom_response
    },
    {
        'type': 0,
        'content': '{ffffff}Want to change your name?',
        'buttons': ['{ffffaa}Yes', 'No, tnx']
    },
]


@Player.on_connect
def on_player_connect(player: Player):
    dc_demo = DialogChain.create(
        for_player=player,
        dialogs=dc_demo_dialogs,
        title='{ffffaa}Default Title',
        on_response=dc_demo_response
    )
    dc_demo.add_to_storage({
        'player_name': '',
        'click_counter': 0
    })
    dc_demo.add_placeholders({
        'error_message': ''
    })
    dc_demo.show()
