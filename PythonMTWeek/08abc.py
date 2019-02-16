"""
abc 抽象基础类

为何要用抽象基础类?

抽象基础类是接口检查的一种形式，比起单独用 hasattr() 检查某些方法更加严格。
通过定义抽象基础类，可以为子类建立一些通用的 API。
抽象基础类可以让不熟悉源代码的人有能力快速熟悉并进一步去写插件扩展，而且可以在一个大型团队或大型项目组中需要保持对所有类的追踪有困难或根本不可能时提供一些帮助。
"""
# ABC (抽象基础类) 是怎么工作的?
# abc 具体的模式是把基础类中的方法抽象标记, 之后注册具体的类作为抽象基础的实现.
# 如果某应用程序或库需要某个特定的 API, 可以用 issubclass() 或 isinstance() 来
# 检查某对象的抽象类.

# 首先定义一个抽象基础类来表示一系列插件中保存和加载数据的 API, 设置这个新的基础
# 类的元类为 ABCMeta, 然后用装饰器为这个类创建公共 API.
import abc

class PluginBase(metaclass=abc.ABCMeta):
# 自动设置元类的功能就直接继承abc.ABC
# class PluginBase(abc.ABC):
    @abc.abstractmethod
    def load(self, input_):
        """从 input_ 中抽取数据并返回一个对象"""

    @abc.abstractmethod
    def save(self, output, data):
        """把 data 保存到 output 中"""

# 注册具体的类
# 分为显示注册和继承的方式注册

# 显示注册
class LoaclBaseClass:
    pass


@PluginBase.register
class RegisteredImplementation(LoaclBaseClass):
    def load(self, input_):
        return input_.read()

    def save(self, output, data):
        return output.write(data)


print('Subclass: ', issubclass(RegisteredImplementation, PluginBase))
print('Instance: ', isinstance(RegisteredImplementation(), PluginBase))

# 继承的方式注册
class SubclassImplementation(PluginBase):
    def load(self, input_):
        return input_.read()

    def save(self, output, data):
        return output.write(data)

print('Subclass: ', issubclass(SubclassImplementation, PluginBase))
print('Instance: ', isinstance(SubclassImplementation(), PluginBase))
# 直接使用继承于基础抽象类的子类有一个好处，就是除非完整的实现抽象类的API否则
# 不会被实例化.

# ABC 中的具体方法
# 抽象基础类还可以提供一些可以被 super() 调用的实现的， 这些实现可以被用在实现
# 基础类时重用某些寻常的逻辑，这样也可以强制让子类实现自己的逻辑.
import io

class ABCWithConcreteImplementation(abc.ABC):

    @abc.abstractmethod
    def retrieve_values(self, input_v):
        print('base class reading data')
        return input_v.read()


class ConcreteOverride(ABCWithConcreteImplementation):

    def retrieve_values(self, input_v):
        base_data = super(ConcreteOverride,
                          self).retrieve_values(input_v)
        print('subclass sorting data')
        response = sorted(base_data.splitlines())
        return response

input_v = io.StringIO("""
    line one
    line two
    line three
""")

reader = ConcreteOverride()
print(reader.retrieve_values(input_v))
print()

# 抽象属性
# 如果某API规范除了方法还有属性, 那么可以将 abstractmethod() 和 property() 结合
# 来标出这个属性.
class Base(abc.ABC):

    @property
    @abc.abstractmethod
    def value(self):
        return 'Should never reach here'

    @property
    @abc.abstractmethod
    def constant(self):
        return 'Should never reach here'


class Implementation(Base):

    @property
    def value(self):
        return 'concrete property'

    constant = 'set by a class attribute'


try:
    b = Base()
    print('Base.value: ', b.value)
except Exception as err:
    print('ERROR:', str(err))

i = Implementation()
print('Implementation.value : ', i.value)
print('Implementation.constant: ', i.constant)
