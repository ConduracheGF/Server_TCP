import asyncio, json, sys

async def listen(reader): #citirea mesajelor de la server
    while True:
        line = await reader.readline()
        if not line: break
        print("<<", line.decode().strip())

async def main():
    host = sys.argv[1] if len(sys.argv)>1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv)>2 else 5001
    reader, writer = await asyncio.open_connection(host, port)
    asyncio.create_task(listen(reader))
    try:
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, input, ">> ")
            if not line: continue
            try:
                obj = json.loads(line)
            except:
                print("JSON invalid!")
                continue
            writer.write((json.dumps(obj)+"\n").encode())
            await writer.drain()
    except KeyboardInterrupt:
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())