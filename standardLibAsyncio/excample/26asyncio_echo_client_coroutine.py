"""
协程和流客户端
"""
import asyncio
import logging
import sys

MESSAGES = [
    b'This is the message.',
    b'It will be sent ',
    b'in parts.',
]
SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()

async def echo_client(address, messages):
    log = logging.getLogger('echo_client')
    log.debug('connecting to {} port {}'.format(*address))
    reader, writer = await asyncio.open_connection(*address)
    # for msg in messages:
        # writer.write(msg)
        # log.debug('sending {!r}'.format(msg))
    # if writer.can_write_eof():
        # writer.write_eof()
    # await writer.drain()

    log.debug('waiting for response')
    while True:
        await asyncio.sleep(1)
        # data = await reader.read(128)
        # if data:
            # log.debug('received {!r}'.format(data))
        # else:
            # log.debug('closing')
            # writer.close()
            # return
            # log.debug('read 0 bytes')
            # writer.write(b'update data')

try:
    event_loop.run_until_complete(
        echo_client(SERVER_ADDRESS, MESSAGES)
    )
finally:
    log.debug('closing event loop')
    event_loop.close()
