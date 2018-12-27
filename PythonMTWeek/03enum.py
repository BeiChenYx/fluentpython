"""
枚举类型
"""
import enum


class BugStatus(enum.Enum):
    """
    创建一个枚举
    """
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_commited = 2
    fix_released = 1

"""
Enum 的成员在类被解析的时候转化为实例，每个实例都有一个
name 属性对应的成员名称，一个 value 属性对应在类中赋值
给成员名称的值
"""
print('\nMember name: {}'.format(BugStatus.wont_fix.name))
print('Member value: {}'.format(BugStatus.wont_fix.value))


# 对enum类的迭代将产生独立的枚举成员
# 成员以它们在类中被定义的顺序逐个产生，成员的名称和值没有
# 以任何方式用来定义他们进行排序。
for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))

actual_state = BugStatus.wont_fix
desired_state = BugStatus.fix_released

print('Equality:',
     actual_state == desired_state,
     actual_state == BugStatus.wont_fix)

print('Identity:',
      actual_state is desired_state,
      actual_state is BugStatus.wont_fix)

# 对枚举成员应用大于和小于比较操作符将抛出TypeError异常
print('Ordered by value:')
try:
    print('\n'.join(' ' + s.name for s in sorted(BugStatus)))
except TypeError as err:
    print('     Cannot sort: {}'.format(err))

# 若想使枚举成员表现得更类似于数字，比如要支持大小比较，则需要使用IntEnum类
class BugStatusInt(enum.IntEnum):
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_commited = 2
    fix_released = 1

print('Ordered by value:')
print('\n'.join(' ' + s.name for s in sorted(BugStatusInt)))


# 唯一值的枚举值
# 具有相同值得 Enum 成员会被当作同一对象的别名引用进行跟踪。
# 别名不会导致 Enum 的迭代器里面出现重复值.
# 如果想要枚举成员只包含唯一值，可以在 Enum 上加上装饰器 @unique

# 编码创建枚举
# 在某种情况下，比起以类定义的方式硬编码枚举，用在编码中动态创建的枚举的方式
# 更加方便。
print('***BugStatusDynamic***')
BugStatusDynamic = enum.Enum(
    value='BugStatusDynamic',
    names=('fix_released fix_commited in_progress '
           'wont_fix invalid incomplete new'),
)

print('Member: {}'.format(BugStatusDynamic.new))
print('\nAll members:')
for status in BugStatusDynamic:
    print('{:15} = {}'.format(status.name, status.value))

# names 可以用一个二元元组或字典来控制成员的值
BugStatusDynamicTupe = enum.Enum(
    value='BugStatusDynamicTupe',
    names=[
        ('new', 7),
        ('incomplete', 6),
        ('invalid', 5),
        ('wont_fix', 4),
        ('in_progress', 3),
        ('fix_commited', 2),
        ('fix_released', 1),
    ],
)
print('***BugStatusDynamicTupe***')
print('All members:')
for status in BugStatusDynamic:
    print('{:15} = {}'.format(status.name, status.value))

# TODO: 同样枚举的值可以用非整数值，具体的用的时候去查文档，不常用;
