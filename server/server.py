import asyncio, logging
from csv import excel

from server.config import Config
from server.auth import check_login
from server.protocol import *
from server.handler import *

async def handle_client(reader, writer):
    #luam adresa clientului si o folosim sa trimitem inapoi mesajele de dat
    peer = writer.get_extra_info("peername")
    logging.info(f"Connection from {peer}")
    user = None
    try: #login loop
        while not user:
            msg = await read_message(reader)
            #daca loginul e valid atunci e introdus in sesiunea de discutie
            if msg.get("cmd") == "login":
                u,p = msg.get("username"), msg.get("password")
                if check_login(u,p):
                    user = u
                    SESSIONS[user] = writer
                    DISCUTII["main"].add(user)
                    await send_message(writer, {"cmd":"login", "ok":True, "discutie":"main"})
                else:
                    await send_message(writer, {"cmd": "login", "ok":False})
            else:
                await send_message(writer, {"error":"login-required"})


            #main loop cereri de client
            while True:
                msg = await read_message(reader)
                cmd = msg.get("cmd")
                if cmd == "join":
                    await handle_join(user, msg.get("discutie", "main"), writer)
                elif cmd == "msg":
                    await handle_msg(user, msg.get("discutie", "main"), msg.get("content", ""))
                elif cmd == "history":
                    await handle_history(user, msg.get("discutie", "main"),writer)
                elif cmd == "quit":
                    await handle_quit(user, writer)
                    break
                else:
                    await send_message(writer, {"error":"unknown-command"})
    except ProtocolError:
        logging.info(f"Protocol error from {peer}")
    finally:
        if user in SESSIONS:
            await handle_quit(user, writer)

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    server = await asyncio.start_server(handle_client, Config.HOST, Config.PORT)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    logging.info(f"Server listening on {addrs}")
    async  with server:
        await  server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
