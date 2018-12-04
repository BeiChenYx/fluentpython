import re 
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    """使用生成器函数实现迭代器的惰性实现"""
    def __init__(self, text):
        # 不再需要words列表
        self.text = text

    def __repr__(self):
        # TODO: reprlib
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        # finditer 函数构建一个迭代器，包含 self.text 中
        # 匹配RE_WORD的单词，产出 MatchObject实例
        """
        for match in RE_WORD.finditer(self.text):
            # 从MatchObject实例中提取正则表达式的具体文本
            yield match.group()
        """
        # 换成生成器表达式，效果更好
        return (match.group() for match in RE_WORD.finditer(self.text))
        """
        针对生成器表达式和生成器函数，使用哪个更好，取决与场景，如果
        生成器表达式要写多行，那么用生成器函数比较好；
        如果要重用，那么生成器函数比较好
        """
