"""
futures.as_completed的使用
"""
from time import sleep, strftime
from concurrent import futures

import tqdm


def display(*args):
    print(strftime('[%H:%M:%s]'), end=' ')
    print((*args))

def loiter(n):
    msg = '{} loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(1)
    msg = '{} loiter({}): done'
    display(msg.format('\t'*n, n))
    return n * 10

def main():
    # max_workers设置最大线程数，不给就默认cpu的个数
    # with futures.ThreadPoolExecutor(max_workers=5) as executor:
    with futures.ThreadPoolExecutor() as executor:
        # 这各字典把各个Future实例映射到任务上，在处理错误时使用
        to_do_map = dict()
        for i in range(10):
            # 每次调用executor.submit方法排定一个可调用
            # 对象的执行时间，然后返回一个Future实例，
            # 第一个参数是可调用的对象，其余的参数是传给
            # 可调用对象的参数;
            future = executor.submit(loiter, i)
            # 把future和任务编号存储在字典中
            to_do_map[future] = i

        # 返回一个迭代器，在期望运行结束后产出期望.
        done_iter = futures.as_completed(to_do_map)
        # done_iter = tqdm.tqdm(done_iter, total=10)

        # 迭代运行结束后的期望
        for future in done_iter:
            try:
                # 在期望上调用result方法，要么返回
                # 可调用对象的返回值，要么抛出可调
                # 用的对象在执行过程中捕获的异常,
                # 这个方法可能会阻塞，等待确定结果,
                # 不过这个实例中不会阻塞，因为
                # as_completed函数只返回已经结束的
                # 期望.
                res = future.result()
            except Exception as err:
                print('%d has error: %s' % (
                    to_do_map[future], str(err))
                )
            else:
                print('result: ', res)


# if __name__ == "__main__":
    # main()
