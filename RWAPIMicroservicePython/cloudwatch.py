import boto3
import logging
import os
import time


class CloudWatchService:
    instance = None

    def __init__(self, region, log_group_name, log_stream_name):
        self.cloudWatchService = boto3.client('logs', region_name=region)
        self.logGroupName = log_group_name
        self.logStreamName = log_stream_name

        if 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
            self.cloudWatchService = boto3.client(
                'logs',
                region_name=region,
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
            )

        self.create_log_group(self.logGroupName)
        self.create_log_stream(self.logGroupName, self.logStreamName)

    @classmethod
    def init(cls, region, log_group_name, log_stream_name):
        if not cls.instance:
            cls.instance = cls(region, log_group_name, log_stream_name)

            cls.instance.logInitPromise.then(
                lambda: logging.debug('CloudWatchService initialized.')
            ).catch(
                lambda error: logging.error(f'CloudWatchService logging initialization failed: {error}')
            )

        return cls.instance

    def create_log_group(self, log_group_name):
        try:
            request_result = self.cloudWatchService.create_log_group(logGroupName=log_group_name)
            logging.debug(f"Log group '{log_group_name}' created successfully.")
        except self.cloudWatchService.exceptions.ResourceAlreadyExistsException:
            logging.debug(f"Log group '{log_group_name}' already exists.")
            return
        except Exception as e:
            logging.warning('Error creating log group:', e)
            raise e

    def create_log_stream(self, log_group_name, log_stream_name):
        try:
            request_result = self.cloudWatchService.create_log_stream(logGroupName=log_group_name,
                                                     logStreamName=log_stream_name)
            logging.debug(f"Log stream '{log_stream_name}' created successfully.")
        except self.cloudWatchService.exceptions.ResourceAlreadyExistsException:
            logging.debug(f"Log stream '{log_stream_name}' already exists.")
            return
        except Exception as e:
            logging.warning('Error creating log stream:', e)
            raise e

    def log_to_cloud_watch(self, log_message):
        put_log_events_params = {
            'logGroupName': self.logGroupName,
            'logStreamName': self.logStreamName,
            'logEvents': [
                {
                    'message': log_message,
                    'timestamp': int(time.time() * 1000)
                }
            ]
        }

        try:
            put_log_events_response = self.cloudWatchService.put_log_events(**put_log_events_params)
            logging.debug('Successfully logged to CloudWatch:', put_log_events_response)
        except Exception as e:
            logging.error('Error logging to CloudWatch:', e)
            raise e
