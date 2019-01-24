"""
logging 模块的使用
"""
import logging
"""
LOG_FILENAME = 'logging_example.out'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
)

logging.debug('This message should go to the log file.')

with open(LOG_FILENAME, 'rt') as f:
    body = f.read()

print('FILE: ')
print(body)

# -----------------------------------------------------------------
# 轮换日志文件
# 上面程序的重复运行脚本会导致更多的信息追加到文件中,要想每次运行
# 时都创建一个新的文件，需要给 basicConfig() 传递 filemode 为 w 的
# 模式， 除了这种方式外，用 RotatingFileHandler 是更好的方式，它会
# 自动创建新文件，同时也不会丢失旧文件

import glob # 使用 Unix shell 规则去查找匹配模式的文件
import logging.handlers


LOG_FILENAME = 'logging_example.out'

# 为 logger 设置我们需要的输出等级
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# 给 logger 添加合适的日志消息处理器
# maxBytes 限制最大字节
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=20, backupCount=5,
)
my_logger.addHandler(handler)

# 写入些日志信息
for i in range(20):
    my_logger.debug('i = %d' % i)

# 查看哪些文件被创建了
logfiles = glob.glob('%s*' % LOG_FILENAME)
for filename in sorted(logfiles):
    print(filename)
# 下面代码要运行，需要注释掉上面的代码
""" 
# -----------------------------------------------------------------
# 日志等级
# logging 另一个有用的功能是可以根据不同的 日志等级 生成不同的消息.
# 也就是说可以在代码中根据调试信息进行不同程度的检测，比如可以设置
# 在生产系统中不显示调试信息.
"""
Level       Value
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
UNSET       0

相应的日志消息只会在处理器或 logger 设置日志等级为此消息的等级或此
消息等级更高时发出。
"""
import sys

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

if len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)

logging.debug('This is a debug message.')
logging.info('This is a info message.')
logging.warning('This is a warning message.')
logging.error('This is an error message.')
logging.critical('This is a critical error message.')

# -----------------------------------------------------------------
# 不同的模块代码的日志信息带上自己的名字
logger1 = logging.getLogger('package1.module1')
logger2 = logging.getLogger('package2.module2')

logger1.warning('This message comes from one module.')
logger2.warning('This comes from another module.')

# -----------------------------------------------------------------
# 日志树
# Logger 实例是以树的形式配置的，不同的 logger 会以不同的名字表示，
# 一般每一个应用程序会定义一个总名称，不同模块中的 logger 都是它的
# 孩子，根 logger 没有名字.
# 树结构用来配置日志非常方便，因为意味着每个 logger 不需要都有自己的
# 处理器，没有处理器的 logger 所发出的消息会被父处理器接受处理. 所以
# 大部分应用程序只需要配置一个根 logger 的处理器，所有的日志信息都会
# 被收集并发送到同一个地方.
# 树结构也允许我们在应用程序的不同部分使用不同的日志等级，处理器和日
# 志格式来管理不同的日志该发送到什么地方.

# -----------------------------------------------------------------
# 集成 warning 模块
# logging 模块通过 captureWarnings() 来集成 warnings , 它会让 warnings
# 将消息通过 logging 系统发送而不是直接输出.
import warnings

logging.basicConfig(
    level=logging.INFO,
)

warnings.warn('This warning is not sent to the logs.')

logging.captureWarnings(True)
warnings.warn('This warning is sent to the logs.')


