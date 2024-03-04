import boto3
from sosw.app import Processor as SoswProcessor, get_lambda_handler, LambdaGlobals


class Processor(SoswProcessor):
    def __call__(self, event, context):
        print("my Function Called")


def lambda_handler(event, context):
    return {"Hello": "World"}


global_vars = LambdaGlobals()
lambda_handler = get_lambda_handler(Processor, global_vars)
