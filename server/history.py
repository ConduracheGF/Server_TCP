from server.config import Config

History = {} #discutie -> lista de nume cu mesaje

def add_message(discutie: str, user:str, message: str):
    if discutie not in History:
        History[discutie] = []
    History[discutie].append((user, message))
    #pastreaza ultima parte din discutie
    if len(History[discutie]) > Config.MAXIM_ISTORIC:
        History[discutie] = History[discutie][-Config.MAXIM_ISTORIC]

def get_history(discutie:str):
    return History.get(discutie, [])