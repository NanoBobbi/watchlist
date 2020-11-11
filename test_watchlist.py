# encoding: utf-8
import unittest
from app import app, db, Movie, User


class WatchlistTestCase(unittest.TestCase):
    """
    docstring
    """

    def setUp(self):
        """
        更新配置
        """
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        # 创建数据库和表
        db.create_all()
        # 创建测试数据，一个用户，一个电影项目
        user = User(name="Test", username="test")
        user.set_password("123")
        movie = Movie(title="Test Movie Title", year="2019")
        # 使用add_all()方法一次添加多个模型类实例，传入列表
        db.session.add_all([user, movie])
        db.session.commit()
        # 创建测试客户端
        self.client = app.test_client()
        # 创建测试命令运行器
        # self.runner = app.test_cli_runner()

    def tearDown(self):
        # 清楚数据库
        db.session.remove()
        db.drop_all()

    # 测试实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config["TESTING"])

    # 测试 404 页面
    def test_404_page(self):
        response = self.client.get("/nothing")
        data = response.get_data(as_text=True)
        self.assertIn("Page Not Found - 404", data)
        self.assertIn("Go Back", data)
        self.assertEqual(response.status_code, 404)

        # 测试主页

    def test_index_page(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("Test's Watchlist", data)
        self.assertIn("Test Movie Title", data)
        self.assertEqual(response.status_code, 200)

        # 测试辅助方法，用于用户登陆

    def login(self):
        self.client.post(
            "/login", data=dict(username="test", password="133"), follow_redirects=True
        )


if __name__ == "__main__":
    unittest.main()
