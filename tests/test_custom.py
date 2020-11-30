import unittest
from tests.config import setup, check

# Uncomment the following code to modify this test class
# class TestCustom(unittest.TestCase):
#
#     ### Do not modify this ###
#     @classmethod
#     def setUpClass(self):
#         self.api_token, self.config, self.product_ref, self.api_instance = setup()
#
#     def setUp(self):
#         self.test_config = check(unittest.TestCase.id(self).rsplit(".")[-1], self.config)
#     ### Do not modify this ###
#
#     # From here you can write your own tests.
#     # For pytest to detect tests the functions must begin with "test_"
#     def test_custom_test(self):
#         # TODO: Do test
#         pass
#         # Failures are marked with pytest.fail("message")
#         # Skipped tests are marked with pytest.skip("message")
#         # Product ref can be accessed with self.product_ref
#         # API instance can be accessed with self.api_instance
#         # API token can be accessed with self.api_token
#         # Variables can be accessed with self.config["variables"]["VARIABLE_NAME"] as defined in Yaml
