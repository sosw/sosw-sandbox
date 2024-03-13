import boto3
import os
import unittest

from unittest import mock
from lambdas.sys_lambda_env_setter.app import Processor
from unittest.mock import MagicMock, patch

os.environ["STAGE"] = "test"
os.environ["autotest"] = "True"


class app_UnitTestCase(unittest.TestCase):
    TEST_CONFIG = {'test': True}

    def setUp(self):
        self.processor = Processor()

    def tearDown(self):
        del(self.processor)

    def test_sample_test(self, boto3_mock):
        self.assertEqual(1, 1)
        self.assertEqual("foo".upper(), "FOO")

    def test_verify_input_event(self):
        input_event = {
            "function": "sample_function",
            "key": "key_value",
            "value": "sample_value"
        }
        with self.assertRaises(AssertionError, msg="Input event should have specific keys"):
            self.processor(input_event)

    @mock.patch("boto3.client")
    def test_response_get_config(self, mock_boto3_client):

        processor_instance = Processor()
        mock_get_func_config = mock.MagicMock(return_value={"my_config_key": "my_config_value"})
        mock_boto3_client.return_value.get_function_configuration = mock_get_func_config

        with mock.patch.object(processor_instance, 'lambda_client', mock_boto3_client):

            response = processor_instance.get_config({"my_config_key": "my_config_value"})

            # Assertions
            self.assertEqual(response, None)
            mock_get_func_config.assert_called_once_with(FunctionName='function')


if __name__ == '__main__':
    unittest.main()
