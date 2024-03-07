import boto3
import logging
from sosw.app import Processor as SoswProcessor, get_lambda_handler, LambdaGlobals


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Processor(SoswProcessor):

    DEFAULT_CONFIG = {
        'init_clients':    ['lambda'],

    }

    lambda_client: boto3.client = None

    def get_config(self, name):
        pass

    def __call__(self, event):

        # Check for variables in event
        assert all(x in event for x in ('function', 'key', 'value')), "Missing required parameters in event"
        # Get current environment variables
        try:
            response = self.lambda_client.get_function_configuration(FunctionName=event['function'])
            if 'Environment' in response:
                current_env_variables = response['Environment']['Variables']
            else:
                current_env_variables = []

        except self.lambda_client.exceptions.ClientError:
            return f"Lambda function '{event['function']}' not found"
        logger.info(current_env_variables)

        # Update or add new environment variables
        if event.get('value') is None:
            current_env_variables.pop(event['key'])
            logger.info("Removing empty variable: %s", event['key'])
        else:
            current_env_variables[event['key']] = event['value']

        # Update lambda function configuration with the new environment variables

        response = self.lambda_client.update_function_configuration(
            FunctionName=event['function'],
            Environment={
                'Variables': current_env_variables
            }
        )
        logger.info(response)


global_vars = LambdaGlobals()
lambda_handler = get_lambda_handler(Processor, global_vars)
