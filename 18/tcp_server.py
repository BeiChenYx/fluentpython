"""
使用asyncio完成简单的tcp服务器
"""
import asyncio


class TcpServer:

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = int(port)
        self.loop = asyncio.get_event_loop()

    def run(self):
        server_coro = asyncio.start_server(
            self.handle_clients,
            host=self.host,
            port=self.port,
            loop=self.loop
        )
        sever = self.loop.run_until_complete(server_coro)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            sever.close()
            self.loop.run_until_complete(sever.wait_closed())
            self.loop.close()

    async def handle_clients(self, reader, writer):
        writer.write('hello world!'.encode('utf-8'))
        # data = yield from reader.readline()
        while True:
            # data = await reader.readline()
            data = await reader.read(1000)
            print(data.decode('utf-8'))
            if data is None:
                print('client close')
                break
    

def main():
    tcp = TcpServer()
    tcp.run()


if __name__ == '__main__':
    main()
