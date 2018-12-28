"""
collections 数据类型容器
"""
# ChainMap: 搜索多个字典
import collections

a = {'a': 'A', 'c': 'C'}
# a = {'a': 'A', 'c': 'C', 'e': 'E'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)
# m = collections.ChainMap(b, a)
print('Individual Values')
print('a = {}'.format(m['a']))
print('b = {}'.format(m['b']))
print('c = {}'.format(m['c']))
print()

print('Keys = {}'.format(list(m.keys())))
print('Values = {}'.format(list(m.values())))
print()

print('Items:')
for k, v in m.items():
    print('{} = {}'.format(k, v))
print()

print('"d" in m: {}'.format(('d' in m)))
# 子映射是搜索的顺序传递给构造函数,所以价值报告的关键“c”来自于一本字典。

"""
ChainMap存储映射列表，它在映射属性中的列表中搜索映射。这个列表是可变的，
因此可以直接添加新的映射，或者更改元素的顺序来控制查找和更新行为。
"""
print('***Reordering***')
print(m.maps)
print('c = {}\n'.format(m['c']))

# 逆转列表
m.maps = list(reversed(m.maps))
print(m.maps)
print('c = {}'.format(m['c']))

"""
链映射不缓存子映射中的值。因此，如果它们的内容被修改，
结果将在访问链图时反映出来。
"""
print('***Updating Values***')
m = collections.ChainMap(a, b)
print('Before: {}'.format(m['c']))
a['c'] = 'E'
print('After: {}'.format(m['c']))

# 也可以通过m直接改变值
m['c'] = 'F'
print('a: ', a)

# 在m中添加新的字典
m2 = m.new_child()
m2['c'] = 'E'
print('m2: ', m2)
# 可以直接在new_child中构造
m3 = m.new_child({'F': 'F'})
print('m3: ', m3)


"""
Counter: Count Hashable Objects
A Counter is a container that keeps track of how many times 
equivalent values are added. It can be used to implement the
same algorithms for which other languages commonly use bag or
multiset data structures.
"""
print('*' * 10)
print(collections.Counter(['a','b','c','a','b','b',]))
print(collections.Counter({'a':2, 'b': 3, 'c': 1}))
print(collections.Counter(a=2, b=3, c=1))

# Counter初始化也可以不需要参数
c = collections.Counter()
print('Initial: ', c)
c.update('abcdaab')
print('Sequence: ', c)
c.update({'a':1, 'd':5})
print('Dict: ', c)

# 当Counter被填充后，就可以使用字典的API了
# 如果键不在那么计数为零，不会报错
for letter in 'abcde':
    print('{} : {}'.format(letter, c[letter]))

# The elements() method returns an iterator that produces all 
# of the items known to the Counter.
c = collections.Counter('extremely')
c['z'] = 0
print(c)
print(list(c.elements()))

# Counter支持计算符
c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'c'])
c2 = collections.Counter('alphabet')

print('C1:', c1)
print('C2:', c2)

print('\nCombined counts: ')
print(c1 + c2)

print('\nSubtraction: ')
print(c1 - c2)

print('\nIntersection (taking positive minimums): ')
print(c1 & c2)

print('\nUnion (taking maximums): ')
print(c1 | c2)


"""
defaultdict: Missing Keys Return a Default Value
The standard dictionary includes the method setdefault() 
for retrieving a value and establishing a default if the
value does not exist. By contrast, defaultdict lets the
caller specify the default up front when the container is initialized.
"""
def default_factory():
    return 'default value'

d = collections.defaultdict(default_factory, foo='bar')
print('d: ', d)
print('foo =>', d['foo'])
print('bar =>', d['bar'])
# TODO: 没明白这个怎么用

"""
deque: 双端队列
双端队列时线程安全的
"""
d = collections.deque('abcdefg')
print('Deque: ', d)
print('Lenght: ', len(d))
print('Left end: ', d[0])
print('Right end: ', d[-1])

d.remove('c')
print('remove(c): ', d)

# 从右边添加
d1 = collections.deque()
d1.extend('abcdefg')
print('extend   :', d1)
d1.append('h')
print('append   :', d1)

# add to the left
d2 = collections.deque()
d2.extendleft(range(6))
print('extendleft: ', d2)
d2.appendleft(6)
print('appendleft: ', d2)

# 两头弹出
print('***' * 20)
print('From the right: ')
d = collections.deque('abcdefg')
while True:
    try:
        print(d.pop(), end=' ')
    except IndexError:
        break
print()

print('\nFrom the left: ')
d = collections.deque(range(6))
while True:
    try:
        print(d.popleft(), end=' ')
    except IndexError:
        break
print()

"""
双端队列的另一个有用的方面是能够在两个方向旋转,跳过一些物品。
"""
d = collections.deque(range(10))
print('Normal: ', d)

d = collections.deque(range(10))
d.rotate(2)
print('Right rotation: ', d)

d = collections.deque(range(10))
d.rotate(-2)
print('Left rotation: ', d)

# 限制队列的大小
import random

random.seed(1)
d1 = collections.deque(maxlen=3)
d2 = collections.deque(maxlen=3)

for i in range(5):
    n = random.randint(0, 100)
    print('n = ', n)
    d1.append(n)
    d2.appendleft(n)
    print('D1: ', d1)
    print('D2: ', d2)


"""
namedtuple: 命名元组
"""
print('***' * 20)

# 常规元组
bob = ('Bob', 30, 'male')
print('Representation: ', bob)

jane = ('Jane', 29, 'female')
print('\nField by index: ', jane[0])

print('\nFields by index: ')
for p in [bob, jane]:
    print('{} is a {} year old {}'.format(*p))


# 定义命名元组, 如果字段名字和Python关键字冲突会抛出ValueError异常
Person = collections.namedtuple('Person', 'name age')

pat = Person(name='Pat', age=12)
print('\nRepresentation: ', pat)
# pat.age= = 21

"""
OrderedDict: 有序字典
An OrderedDict is a dictionary subclass that remembers the order 
in which its contents are added.
"""
print('*' * 20)

# 在3.6字典创建的是跟踪顺序的，但是不能依赖这个特性
print('Regular dictionary: ')
d = {}
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)

print('\nOrderedDict: ')
d = collections.OrderedDict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)

# 常规的dict看着平等的内容在测试。一个OrderedDict还考虑的顺序添加的条目。
print('dict     :', end=' ')
d1 = {}
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = {}
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'
print(d1 == d2)

print('OrderedDict: ', end=' ')
d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'
d2 = collections.OrderedDict()
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'
print(d1 == d2)

# 可以使用move_to_end()将键移动到序列的开头或末尾，
# 从而更改OrderedDict中的键的顺序
d = collections.OrderedDict(
    [('a', 'A'), ('b', 'B'), ('c', 'C')]
)

print('Before: ')
for k, v in d.items():
    print(k, v)

d.move_to_end('b')

print('\nmove_to_end():')
for k, v in d.items():
    print(k, v)

d.move_to_end('b', last=False)

print('\nmove_to_end(last=False): ')
for k, v in d.items():
    print(k, v)



