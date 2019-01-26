"""
第三方库 transitions 状态机的使用
pip install transitions
https://github.com/pytransitions/transitions
"""
import random
from transitions import Machine


class NarcolepticSuperhero(object):
    """状态机的简单的示例"""

    # 定义一些状态
    states = ['asleep', 'hanging out', 'hungry',
              'sweaty', 'saving the world']
    def __init__(self, name):
        # 给个名字，随意取
        self.name = name

        # 今天完成了什么?
        self.kittens_rescued = 0

        # 初始化一个状态机
        self.machine = Machine(
            model=self,
            states=NarcolepticSuperhero.states, initial='asleep'
        )

        # 添加一些转换
        self.machine.add_transition(
            trigger='wake_up', source='asleep', dest='hanging out'
        )
        self.machine.add_transition('work_out', 'hanging out', 'hungry')
        self.machine.add_transition('eat', 'hungry', 'hanging out')
        self.machine.add_transition(
            'distress_call', '*', 'saving the world',
            before='chang_into_super_secret_costume'
        )
        self.machine.add_transition(
            'compete_mission', 'saving the word', 'sweaty',
            after='update_journal'
        )
        self.machine.add_transition(
            'clean_up', 'sweaty', 'asleep', conditions=['is_exhausted']
        )
        self.machine.add_transition('clean_up', 'sweaty', 'hanging out')
        self.machine.add_transition('nap', '*', 'asleep')

    def update_journal(self):
        self.kittens_rescued += 1

    def is_exhausted(self):
        return random.random() < 0.5

    def chang_into_super_secret_costume(self):
        print("Beauty, eh?")

# --------------------------------------------------------------------
# The non-quickstart
# Basic initialization
# 一个简单的状态机
class Matter(object):
    pass

lump = Matter()
machine = Machine(
    model=lump,
    states=['solid', 'liquid', 'gas', 'plasma'],
    initial='solid'
)
# 至此，已经完成了一个最小的状态机，但是不能切换状态，因为没有
# 定义 transitions
# 添加 transitions
states=['solid', 'liquid', 'gas', 'plasma']
transitions = [
    {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid'},
    {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
    {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'},
]

# initialize
machine = Machine(
    lump, states=states, transitions=transitions, initial='liquid'
)

# States: 状态机的核心
# 初始化和修改状态的几种方式:
#   通过字符串
#   直接使用 State 对象
#   使用一个字典
from transitions import State
states = [
    State(name='solid'), # 通过State创建对象
    'liquid',            # 通过字符串
    {'name': 'gas'},     # 通过字典
]
machine = Machine(lump, states)

# 也可以通过 add_states 来添加状态
machine = Machine(lump)
solid = State('solid')
liquid = State('liquid')
gas = State('gas')
machine.add_states([solid, liquid, gas])
# 状态机的状态，应该只初始化一次，不能改动，除非重新创建

# Callbacks
# 一个状态在进入和退出都可以调用回调, 可以在初始化添加或者之后添加
