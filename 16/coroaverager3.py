"""
使用嵌套链接的方式完成统计:
    统计任务:
    从一个字典中读取虚构的七年级男女学生的
    体重和升高。计算平均值，然后生成一个报告
"""
from collections import namedtuple


Result = namedtuple('Result', 'count, average')

def averager():
    """子生成器"""
    total = 0.0
    count = 0
    average = None
    while True:
        # main 函数中的客户代码发送的各个值绑定
        # 到这里的term变量上.
        term = yield
        # 终止条件，如果没有，则会使yield from调用这个协程
        # 的生成器永远阻塞.
        if term is None:
            break
        total += term
        count += 1
        average = total / count

    # 返回的Result会成为grouper函数中yield from表达式的值
    return Result(count, average)

def grouper(results, key):
    """委派生成器"""
    while True:
        # 这个循环每次迭代时会新建一个averager实例
        # 每个实例都是作为协程使用的生成器对象.
        # grouper 发送的每个值都会经由 yield from 处理,
        # 通过管道传给averager实例.grouper 会在yield from
        # 表达式处暂停, 等待averger 实例处理客户端发来的值。
        # averager 实例运行完毕后，返回的值绑定到 results[key]
        # 上. while 循环会不断创建averager实例，处理更多的值.
        results[key] = yield from averager()

def main(data):
    """客户端代码，即调用方"""
    results = {}
    for key, values in data.items():
        # group 是调用grouper函数得到的生成器对象,
        # 传给grouper 第一个参数是results, 用于收集
        # 结果，第二个参数是一个键，group作为协程使用.
        group = grouper(results, key)
        # 激活 group 协程
        next(group)
        for value in values:
            # 把各个value 传给grouper, 传入的值最终到达
            # averager 函数中 term = yield 那行，grouper
            # 永远不知道传入的值是什么。
            group.send(value)
        # 把 None 传入 grouper, 导致当前的averager实例终止，
        # 也让 grouper 继续运行，再创建一个averager实例，
        # 处理下一组值.
        group.send(None)

    print(results)
    report(results)

def report(results):
    """输出报告"""
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{} '.format(
              result.count, group, result.average, unit)
        )


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

if __name__ == "__main__":
    main(data)
