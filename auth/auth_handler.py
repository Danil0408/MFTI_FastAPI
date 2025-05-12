import shortuuid
def create_token(player_id:str)-> str:
    return str(player_id) + shortuuid.uuid()