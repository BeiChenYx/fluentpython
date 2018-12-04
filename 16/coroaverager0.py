"""
协程:
    yield: 字典解释为 产出和让步;
    对于python生成器中的yield来说, 这两个含义都成立。
    yield item这行代码会产出一个值, 提供给next(...)的
    调用方, 此外，还会做出让步, 暂停执行生成器，让调用
    方继续工作，直到需要使用另一个值时再调用next(),
    调用方会从生成器中拉取值。

    从语法上看协程和生成器类似，都是定义体中包含yield
    关键字的函数，但，协程中yield通常再表达式的右边,
    可以产出值，也可以不产出---如果yield后面没有表达式
    那么生成器产出None .
    协程可能会从调用方接收数据，不过调用方把数据提供给
    协程使用的是 .send(datum)方法，而不是next()

    从根本上把 yield 视作控制流程的方式，这样就好理解协程了.
"""
from functools import wraps
from collections import namedtuple


Result = namedtuple('Result', 'count average')

class DemoException(Exception):
    pass

# 定义个计算移动平均值的协程
# def averager():
    # total = 0.0
    # count = 0
    # average = None
    # while True:
        # term = yield average
        # total += term
        # count += 1
        # average = total / count

def coroutine(func):
    """
    装饰器: 向前执行到第一个yield表达式激活func
    """
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

# @coroutine
# def averager():
    # total = 0.0
    # count = 0
    # average = None
    # while True:
        # term = yield average
        # total += term
        # count += 1
        # average = total / count

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException: # 特别处理DemoException异常
            print('*** DemoException handled. Continuing...')
        else: # 如果没有异常, 那么显示接收到的值
            print('-> coroutine received: {!r}'.format(x))
        finally:
            print('-> coroutine ending')
    # 这一行永远不会执行, 因为只有未处理的异常才会终止那个
    # 无限循环, 而一旦出现未处理的异常，协程立即终止
    raise RuntimeError('This line should never run.')

def averager():
    """演示协程返回值"""
    total = 0.0
    count = 0
    average = None
    while True:
        # 这一版不产出值
        term = yield
        # 接收到None会终止循环，导致协程结束，生成器对象会
        # 抛出 StopIteration 异常。异常对象的 value 属性保存
        # 着返回的值
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    # return 表达式的值会偷偷传给调用方， 赋值给
    # StopIteration 异常的一个属性。这样做有点不合常理
    # 但能保留生成器对象的常规行为--耗尽时抛出 StopIteration异常
    return Result(count, average)
    """
    如何获取协程返回值呢?
    coro_avg = averager()
    next(coro_avg)
    coro_avg.send(10)
    coro_avg.send(30)
    coro_avg.send(6.5)
    try:
        coro_avg.send(None)
    except StopIteration as exc:
        # result 中获取了协程的返回值
        result = exc.value
        print(result) # >> Result(count=3, average=15.5)
    """
    """
    上面这种获取协程返回值的方法绕了个圈子，因此才有了
    yield from结构，其在内部自动捕捉StopIteration异常。
    对于yield from结构来说，解析器不仅会捕获 StopIteration
    异常，还会把 value 属性的值变成 yield from 表达式的值.
    """

"""
使用yield from
yield from 作用比yield多很多，因此在python3.5还是3.6中使用
await代替, 至关重要的一点: 在生成器gen中使用yield from subgen()
时, subgen 会获得控制权, 把产出的值传递给 gen 的调用方，即调用
方可以直接控制 subgen ， 与此同时， gen会阻塞，等待 subgen 终止.
"""
# yield form 可以简化for 循环中的yield表达式
def gen():
    for c in 'AB':
        yield c
    for i in range(1, 3):
        yield i

"""
In [9]: list(gen())
Out[9]: ['A', 'B', 1, 2]
"""
# 可以简化为
def genFrom():
    yield from 'AB'
    yield from range(1, 3)

"""
In [10]: list(genFrom())
Out[10]: ['A', 'B', 1, 2]
"""

# 使用 yield from 链接可迭代的对象
def chain(*iterables):
    for it in iterables:
        yield from it

"""
In [13]: s = 'ABC'

In [14]: t = tuple(range(3))

In [15]: list(chain(s,t))
Out[15]: ['A', 'B', 'C', 0, 1, 2]
"""
"""
yield from x 表达式对 x 对象所做的第一件事是，调用iter(x),
从中获取迭代器，因此， x 可以是任何可迭代的对象。
yield from 的主要功能:
    打开双向通道，把最外层的调用方与最内层的子生成器连接
    起来，这样二者可以直接发送和产出值，还可以直接传入异常，
    而不用在位于中间的协程中添加大量处理异常的样板代码.
"""
