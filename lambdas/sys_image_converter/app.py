import boto3
import logging
from sosw.app import Processor as SoswProcessor, get_lambda_handler, LambdaGlobals
from PIL import Image
from io import BytesIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Processor(SoswProcessor):

    DEFAULT_CONFIG = {
        'init_clients':    ['lambda'],
    }

    s3_client: boto3.client = None

    def get_config(self, name):
        pass

    def __call__(self, event):
        # Check for variables in event
        assert all(
            x in event for x in ('bucket_name', 'input_key', 'output_key')), "Missing required parameters in event"
        # Get image from S3 bucket
        response = self.s3_client.get_object(Bucket=event['bucket_name'], Key=event['input_key'])
        image_data = response['Body'].read()

        # Convert image to PNG and WebP formats
        image = Image.open(BytesIO(image_data))
        webp_data = BytesIO()
        image.save(webp_data, format="WebP")

        # Upload converted image to S3 bucket
        self.s3_client.put_object(Bucket=event['bucket_name'], Key=event['output_key'], Body=webp_data.getvalue())

    """
    Sample event
    {
        "bucket_name": "your_bucket_name",
        "input_key": "path/to/original/image.png",
        "output_key": "path/to/converted/image.webp"
    }
    """


global_vars = LambdaGlobals()
lambda_handler = get_lambda_handler(Processor, global_vars)
