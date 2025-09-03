import json

class ProtocolError(Exception):
    pass #exceptii pentru mesaje gresite si conectiuni inchise

async def read_message(reader): #citire de la client a mesajului linie cu linie
    raw = await reader.readline()
    if not raw:
        raise ProtocolError("EOF")
    try:
        return json.loads(raw.decode().strip())
    except Exception:
        raise ProtocolError("Invalid JSON")

async def send_message(writer, object:dict):
    line = json.dumps(object) + "\n" #transforma dictionarul in string json cu terminator
    writer.write(line.encode())#trimite mesajul la client
    await writer.drain() #golire buffer