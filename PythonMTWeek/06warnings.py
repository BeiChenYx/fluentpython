"""
warnings 模块学习
向用户提供有关运行程序时遇到的问题的非致命警报
最好使用 logging 模块提供面向用户的消息
"""
# 类别和过滤
# 使用内置异常类 Warning 的子类对警告进行分类
# exceptions 模块可以通过 warning 的子类添加自定义警告.
# 警告根据 filter 设置进行处理。过滤器由五部分组成:
#   actcion, message, category, module, line number
# 过滤器的 message 部分是一个正则表达式，用于匹配警告文本,
# category 是异常类的名称， module 包含一个正则表达式, 用于
# 匹配生成警告的模块名称，并且 line number 可用于更改特定事件
# 时发送时的处理. 生成警告时，会将其与所有已注册的过滤器进行
# 比较，匹配的第一个过滤器控制警告所采取的操作，如果没有匹配
# 的过滤器，则采用默认操作.
# 警告过滤器操作
#   动作            执行内容
#   error           将warning转换为exception
#   ignore          关闭 Warning
#   always          永远提示 Warning
#   default         在每一个位置warning第一次生成时打印出来
#   module          在每一个Module里warning第一次生成时打印出来
#   once            warning第一次生成时打印出来
import warnings

print('Before the warning')
warnings.warn('This is a warning message.')
print('After the warning')
# 会打印警告后，默认行为是继续gin果果该点并运行程序的其余部分，
# 可以使用过滤器更改行为.

# warnings.simplefilter('error', UserWarning)
# print('Before the warning')
# warnings.warn('This is a warning message.')
# print('After the warning')
# 也可以通过命令行选项来控制过滤器行为
# python3 -u -W "error::UserWarning::0" 06warnings.py

# 使用模式过滤
# 要以编程方式过滤更复杂的规则，使用 filterwarnings(), 将正则
# 表达式作为 message 参数, 正则不分大小写字母
warnings.filterwarnings('ignore', '.*do not.*', )

warnings.warn('Show this message.')
warnings.warn('Do not show this message.')

# 其他消息传递函数
# 通常警告会打印到 sys.stderr , 通过替换 warnings 模块中的
# showwarning() 函数来改变这种行为.
import logging

def send_warnings_to_log(message, category, filename, lineno,
                         file=None, line=None):
    logging.warning('%s:%s: %s:%s', filename, lineno,
                    category.__name__, message)

logging.basicConfig(level=logging.INFO)
old_showwarning = warnings.showwarning
warnings.showwarning = send_warnings_to_log
warnings.warn('message')

# 格式化，如果警告应该发送到标准错误流，但需要重新格式化
# 需要替换 formatwarning()
def warning_on_one_line(message, category, filename, lineno,
                        file=None, line=None):
    return '-> {}:{}: {}:{}'.format(
        filename, lineno, category.__name__, message
    )

warnings.warn('Warning message, before')
warnings.formatwarning = warning_on_one_line
warnings.warn('Warning message, after')

