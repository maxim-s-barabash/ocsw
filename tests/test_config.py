import os
import unittest

from ocsw.utils.config import Config


def rm(path):
    if os.path.exists(path):
        os.unlink(path)


class TestConfig(unittest.TestCase):
    def test_empty_arguments(self):
        data = dict()
        config = Config(**data)
        self.assertEqual(config.__dict__, data)

    def test_arguments(self):
        data = dict(
            base_url="API", login="User", token="Token", company="Company"
        )
        config = Config(**data)
        self.assertEqual(config.__dict__, data)

    def test_defaults_attr(self):
        config = Config().as_dict()
        self.assertTrue("base_url" in config)
        self.assertTrue("login" in config)
        self.assertTrue("token" in config)
        self.assertTrue("company" in config)

    def test_store(self):
        data = dict(
            base_url="API", login="User", token="Token", company="Company"
        )
        cfg_path = ".test_store"
        rm(cfg_path)
        Config(**data).save(cfg_path)
        config = Config(cfg_path)
        self.assertEqual(config.as_dict(), data)
        self.assertEqual(str(config), str(data))
        rm(cfg_path)


if __name__ == "__main__":
    unittest.main()
