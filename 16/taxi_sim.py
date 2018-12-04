"""出租车仿真"""
import random
import collections
import queue
import argparse


# 发车间隔
DEPARTURE_INTERVAL = 5
# 默认出租车的数量
DEFAULT_NUMBER_OF_TAXIS = 3
# 默认结束事件
DEFAULT_END_TIME = 180
# 搜索时间
SEARCH_DURATION = 5
# 行程
TRIP_DURATION = 20

Event = collections.namedtuple('Event', 'time proc action')

def taxi_process(ident, trips, start_time=0):
    """
    每次改变状态时创建事件, 把控制权让给仿真器
    每辆出租车调用一次 taxi_process 函数，创建
    一个生成器对象，表示各辆出租车的运营过程。
    ident 是出租车的编号。trips 是出租车回家之
    前的行程数量，start_time是出租车离开车库的
    时间.
    """
    # 产出的第一个 Event 是 'leave garage'. 执行到这一行时，
    # 协程会暂停，让仿真主循环着手处理排定的下一个事件，需要
    # 重新激活这个进程时，主循环会发送(使用send方法)当前的仿
    # 真事件，赋值给time
    time = yield Event(start_time, ident, 'leave garage')

    # 每次行程都会执行一遍这个代码块
    for i in range(trips):
        # 产出一个 Event 实例，表示拉倒乘客了，协程在这里暂停，
        # 需要重新激活这个协程时，主循环发送当前时间.
        time = yield Event(time, ident, 'pick up passenger')
        # 产出一个 Event实例，表示乘客下车了，协程在这里暂停，
        # 等待主循环发送时间，然后重新激活.
        time = yield Event(time, ident, 'drop off passenger')

    # 指定的行程数量完成后，for循环结束，最后产出'going home'
    # 事件,此时，协程最后一次暂停，仿真主循环发送时间后，协程
    # 重新激活;
    yield Event(time, ident, 'going home')
    # 出租车进程结束
    # 协程执行到最后时，生成器对象抛出StopIteratio异常.


class Simulator:

    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()
        # taxi_process创建的taxi对象，再用字典推到封装
        self.procs = dict(procs_map)

    def run(self, end_time):
        """排定并显示事件, 直到时间结束"""
        # 排定各辆出租车的第一个事件
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)

        # 这个仿真系统的主循环
        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print('*** end of events ***')
                break

            current_event = self.events.get()
            sim_time, proc_id, previous_action = current_event
            print('taxi:', proc_id, proc_id * ' ', current_event)
            active_pro = self.procs[proc_id]
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_pro.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))

def compute_duration(previous_action):
    """使用指数分布计算动作持续时间"""
    if previous_action in ['leave garage', 'drop off passenger']:
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unknown previous_action: %s' % previous_action)
    return int(random.expovariate(1/interval)) + 1

def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
        seed=None):
    """初始化随机生成器，构建过程并运行仿真"""
    if seed is not None:
        random.seed(seed)
    # 使用字典推导式来生成taxis
    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL)
             for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Taxi fleet simulator.')
    parser.add_argument('-e', '--end-time', type=int,
                        default=DEFAULT_END_TIME,
                        help='simulation end time; default = %s'
                        % DEFAULT_END_TIME)
    parser.add_argument('-t', '--taxis', type=int,
                        default=DEFAULT_NUMBER_OF_TAXIS,
                        help='number of taxis running; default = %s'
                        % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='random generator seed (for testing)')

    args = parser.parse_args()
    main(args.end_time, args.taxis, args.seed)


"""
root@yx:~/workspace/fluentPython/16# python taxi_sim.py -s 3 -e 120
taxi: 0  Event(time=0, proc=0, action='leave garage')
taxi: 0  Event(time=2, proc=0, action='pick up passenger')
taxi: 1   Event(time=5, proc=1, action='leave garage')
taxi: 1   Event(time=8, proc=1, action='pick up passenger')
taxi: 2    Event(time=10, proc=2, action='leave garage')
taxi: 2    Event(time=15, proc=2, action='pick up passenger')
taxi: 2    Event(time=17, proc=2, action='drop off passenger')
taxi: 0  Event(time=18, proc=0, action='drop off passenger')
taxi: 2    Event(time=18, proc=2, action='pick up passenger')
taxi: 2    Event(time=25, proc=2, action='drop off passenger')
taxi: 1   Event(time=27, proc=1, action='drop off passenger')
taxi: 2    Event(time=27, proc=2, action='pick up passenger')
taxi: 0  Event(time=28, proc=0, action='pick up passenger')
taxi: 2    Event(time=40, proc=2, action='drop off passenger')
taxi: 2    Event(time=44, proc=2, action='pick up passenger')
taxi: 1   Event(time=55, proc=1, action='pick up passenger')
taxi: 1   Event(time=59, proc=1, action='drop off passenger')
taxi: 0  Event(time=65, proc=0, action='drop off passenger')
taxi: 1   Event(time=65, proc=1, action='pick up passenger')
taxi: 2    Event(time=65, proc=2, action='drop off passenger')
taxi: 2    Event(time=72, proc=2, action='pick up passenger')
taxi: 0  Event(time=76, proc=0, action='going home')
taxi: 1   Event(time=80, proc=1, action='drop off passenger')
taxi: 1   Event(time=88, proc=1, action='pick up passenger')
taxi: 2    Event(time=95, proc=2, action='drop off passenger')
taxi: 2    Event(time=97, proc=2, action='pick up passenger')
taxi: 2    Event(time=98, proc=2, action='drop off passenger')
taxi: 1   Event(time=106, proc=1, action='drop off passenger')
taxi: 2    Event(time=109, proc=2, action='going home')
taxi: 1   Event(time=110, proc=1, action='going home')
*** end of events ***
"""
