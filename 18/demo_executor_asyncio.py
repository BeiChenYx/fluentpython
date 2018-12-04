"""
futures.as_completed的使用
"""
import asyncio
from time import sleep, strftime
from concurrent import futures


@asyncio.coroutine
def display(*args):
    print(strftime('[%H:%M:%s]'), end=' ')
    print((*args))

@asyncio.coroutine
def loiter(n):
    msg = '{} loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(1)
    msg = '{} loiter({}): done'
    display(msg.format('\t'*n, n))
    return n * 10

def main():
    loop = asyncio.get_event_loop()
    to_do = [loiter(i) for i in range(10)]
    wait_coro = asyncio.wait(to_do)

    # run_until_complete 返回两个元素的元组,
    # 第一个是已经完成的期物第二个是未完成的期物
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    print(res)


if __name__ == "__main__":
    main()


