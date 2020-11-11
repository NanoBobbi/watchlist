# encoding: utf-8
def sayHello(to=None):
    """
    仅用来测试的的函数，显示一段字符串
    """
    if to:
        return 'Hello, %s!' % to
    return 'Hello!'