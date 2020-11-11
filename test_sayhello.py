# encoding: utf-8
import  unittest
from module_foo import  sayHello

class SayHelloTestCase(unittest.TestCase):
    """
    测试用例
    """
    def setUp(self):
        """
        测试固件
        setUp() 方法会在每个测试方法执行前被调用
        准备弹药、规划战术的工作就要在 setUp()方法里完成
        """
        pass
    def tearDown(self):
        """
        测试固件
        tearDown() 方法则会在每 一个测试方法执行后被调用
        打扫战场则要在 tearDown()
        """
        pass

    def test_sayHello(self):
        rv = sayHello()
        self.assertEqual(rv, 'Hello!')

    def test_sayHello_to_sb(self):
        rv = sayHello(to='Grey')
        self.assertEqual(rv, 'Hello, Grey!')

if __name__ == '__main__':
    unittest.main()

