import boto3
import json
import os
import logging
from datetime import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth



# Initialize the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS services clients
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')

# Elasticsearch/OpenSearch configuration
host = 'search-photos-orc4p7tbe7o6btwyt4l6xm4ugq.aos.us-east-1.on.aws'
region = 'us-east-1'
es_index = 'photos'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
#master_username = os.environ['MASTER_USERNAME']  # Environment variable for the master user's username
#master_password = os.environ['MASTER_PASSWORD']  # Environment variable for the master user's password
#auth = (master_username, master_password)
#awsauth = AWSRequestsAuth(aws_access_key='AKIATCKAPJWKJX6P6YPC',
               #       aws_secret_access_key='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',
                    ##  aws_host=host,
                    #  aws_region='us-east-1',
                    #  aws_service='es')
#auth = ('Madhurimhw3','x40Q6$U_')
es = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def lambda_handler(event, context):
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Processing file: {object_key} in bucket: {bucket_name}")
        
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        #json.loads
        custom_labels = response.get('Metadata', {}).get('customlabels', '[]')
        
        rekognition_response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
            MaxLabels=10
        )
        
        detected_labels = [label['Name'] for label in rekognition_response['Labels']]
        print(detected_labels )
        labels = list(set(custom_labels + detected_labels))
        print(labels)
        
        
        doc = {
            'objectKey': object_key,
            'bucket': bucket_name,
            'createdTimestamp': datetime.now().isoformat(),
            'labels': labels
        }
        
        es_response = es.index(index=es_index, body=doc)
        logger.info(f"Document indexed successfully in OpenSearch: {es_response}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Document indexed successfully.')
        }
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error occurred processing the Lambda function')
        }
