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

