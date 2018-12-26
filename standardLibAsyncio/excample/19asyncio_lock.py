"""
Lock
"""
import asyncio
import functools


def unlock(lock):
    print('callback releasing lock')
    lock.release()

async def corol(lock):
    print('corol waiting for the lock')
    with await lock:
        print('corol acquired lock')
    print('corol released lock')

async def coro2(lock):
    print('coro2 waiting for the lock')
    await lock
    try:
        print('coro2 aquired lock')
    finally:
        print('coro2 released lock')
        lock.release()

async def main(loop):
    lock = asyncio.Lock()
    print('acquiring the lock before starting coroutines')
    await lock.acquire()
    print('lock acquired: {}'.format(lock.locked()))
    loop.call_later(0.1, functools.partial(unlock, lock))

    print('waiting for coroutines')
    await asyncio.wait([corol(lock), coro2(lock)])

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
