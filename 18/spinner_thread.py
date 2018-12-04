"""
使用线程实现旋转指针
"""
import threading
import itertools
import time
import sys


class Signal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        # 需要不断刷新才能及时看到输出
        flush()
        # \x08 是退格，将光标移回去
        write('\x08' * len(status))
        time.sleep(0.1)
        
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():
    """等待函数"""
    # 假装等待I/O一段时间
    time.sleep(3)
    return 42

def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner)
    spinner.start()
    result = slow_function()
    slow_function()
    signal.go = False
    spinner.join()
    return result

def main():
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()
