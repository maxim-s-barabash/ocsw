import os
import unittest

from ocsw.utils.secrets import mask_secrets


def rm(path):
    if os.path.exists(path):
        os.unlink(path)


class TestConfig(unittest.TestCase):
    def test_common_mask_secrets(self):
        masked_value = "***"
        data = [
            {"secret": 12345678},
            [{"secret": 3456890}],
            {"not_secret": "hello", "key": [{"secret": 12345678}]},
        ]
        ref = [
            {"secret": masked_value},
            [{"secret": masked_value}],
            {"not_secret": "hello", "key": [{"secret": masked_value}]},
        ]

        masked_data = mask_secrets(data, ["secret"], masked_value)
        self.assertEqual(masked_data, ref)

    def test_common_mask_secrets2(self):
        masked_value = "***"
        data = {
            "secret": [
                {"secret": 12345678},
                [{"secret": 3456890}],
                {"not_secret": "hello"},
            ]
        }
        ref = {"secret": masked_value}

        masked_data = mask_secrets(data, ["secret"], masked_value)
        self.assertEqual(masked_data, ref)


if __name__ == "__main__":
    unittest.main()
