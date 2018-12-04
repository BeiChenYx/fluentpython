"""
使用asyncio实现旋转指针
"""
import asyncio
import itertools
import sys


@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))

        try:
            # 使用asyncio.sleep不会阻塞事件循环
            yield from asyncio.sleep(0.1)
        # 接收到了asyncio.CancelledError说明发出了取消
        # 请求，因此退出循环
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))

@asyncio.coroutine
def slow_function():
    # 假装等待 I/O 一段时间
    yield from asyncio.sleep(3)
    return 42

@asyncio.coroutine
def supervisor():
    # asyncio.async函数排定spin协程的运行时间，
    # 使用一个Task对象包装spin协程，并立即返回
    spinner = asyncio.async(spin('thinking!'))
    print('spinner object:', spinner)
    result = yield from slow_function()
    spinner.cancel()
    return result

def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
"""
在 asyncio 包中，期物和协程关系紧密，因为可以使用 yield from 
从 asyncio.Future 对象中产出结果。这就意味着, 如果 foo 是协程
函数，抑或是返回 Future 或 Task 实例的普通函数，那么可以这样写
res = yield from foo()  这是 asyncio 包的API 中很多地方可以互换
协程与期物的原因之一.

为了执行这些操作，必须排定协程的运行时间，然后使用 asyncio.Task
对象包装协程。对协程来说，获取 Task 对象有两种主要方式.
    asyncio.async(coro_or_future, *, loop=None)
    这个函数统一了协程和期物:
    coro_or_future: 这参数可以是协程或者期物, 如果是Future 或
    Task 对象，那就原封不动的返回，如果是协程，那么 async 函数
    会调用 loop.create_task(...) 方法创建 Task 对象， loop是
    关键字参数，为可选，用于传入事件循环；如果没有传入，那么
    async 函数会通过调用 asyncio.get_event_loop() 函数获得循环
    对象。

    BaseEventLoop.create_task(coro)
    这个方法排定协程的执行事件，返回一个 asyncio.Task 对象,
    如果在自定义的 BaseEventLoop 子类上调用, 返回的对象可能
    是外部库中与 Task 类兼容的某个类的实例.
"""


