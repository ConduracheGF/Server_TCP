import logging
from server.protocol import send_message
from server.history import add_message, get_history

SESSIONS = {}#username -> writer
DISCUTII = {"main":set()} #discutii -> set(user)

async def broadcast(discutie:str, payload:dict, exclude:str=None):
    #trimite mesajul tuturor dintr-un grup de discutii
    for u in list(DISCUTII.get(discutie, [])):
        if u == exclude:
            continue
        w = SESSIONS.get(u)
        if w:
            await send_message(w, payload)

async def handle_join(user:str, discutie: str, writer):
    #adauga user
    DISCUTII.setdefault(discutie, set()).add(user)
    await send_message(writer, {"cmd":"join", "ok":True, "discutie":discutie})
    await broadcast(discutie, {"evt":"join", "user":user}, exclude=user)

async def handle_msg(user:str, discutie:str, mesaj:str):
    #salvare mesaj in istoric
    add_message(discutie,user,mesaj)
    await broadcast(discutie, {"evt":"msg", "discutie":discutie, "from":user, "mesaj":mesaj})

async def handle_history(user:str, discutie: str, writer):
    #trimite istoricul cerut solicitarii
    history = [{"from":u, "content":m} for u, m in get_history(discutie)]
    await send_message(writer, {"cmd":"history", "discutie":discutie, "messages": history})

async def handle_quit(user: str, writer): #deconectarea userului de la discutii si sesiuni
    for r in DISCUTII.values():
        r.discard(user)
    SESSIONS.pop(user, None)
    await send_message(writer, {"cmd":"quit", "ok":True})
    writer.close()
    await writer.wait_closed()
    logging.info(f"{user} disconnected")