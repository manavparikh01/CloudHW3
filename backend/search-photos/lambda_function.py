import json
import logging
import random
import boto3
import botocore
# from aws_requests_auth.aws_auth import AWSRequestsAuth
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
#from elasticsearch import Elasticsearch, RequestsHttpConnection

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a Lex V2 runtime client
lex_v2 = boto3.client('lexv2-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    # slots = event['sessionState']['intent']['slots']
    

    #q1 = "sunset and birds"  # Example query
    # q = event[q]
    # labels = get_labels(q)
    print("what is the event", event)
    
    if 'queryStringParameters' in event:
        # Access the 'q' parameter from 'queryStringParameters'
        q = event['queryStringParameters']['q']
        print("query", q)
        labels = get_labels(q)
        print("labels", labels)
        # Now 'q' contains the value of the 'q' query parameter
    else:
        # If 'queryStringParameters' doesn't exist, handle the error
        return {
            'statusCode': 400,
            'body': 'No query parameter found'
        }
    
    print("length", len(labels))
    
    if len(labels) != 0:
        print("hehe")
        img_path = get_photo_path(labels)
        
    if not img_path:
        return{
            'statusCode':200,
            "headers": {"Access-Control-Allow-Origin":"*",
                "Content-Type": "application/json"
            },
            'body': json.dumps('No Results found')
        }
    else:    
        return{
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin":"*",
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                "results": img_path
                # 'imagePaths':img_path,
                # 'userQuery':q,
                # 'labels': labels,
            }),
            # 'isBase64Encoded': False
        }
    
    

def get_labels(query):
    sample_string = 'pqrstuvwxyabdsfbc'
    user_id = ''.join((random.choice(sample_string)) for _ in range(8))

    print(query)

    try:
        # Call post_text operation for Lex V2
        response = lex_v2.recognize_text(
            botId='LAD0SZBA6I',
            botAliasId='TSTALIASID',
            localeId='en_US',  # Language/locale of the input text
            sessionId=user_id,
            text=query
        )
        print("lex-response", response)
        
        data = response

# Extract interpreted values of "trees" and "birds"
        interpreted_values = []
        for value in data["sessionState"]["intent"]["slots"]["images"]["values"]:
            interpreted_values.append(value["value"]["interpretedValue"])

        print(interpreted_values)
        return interpreted_values

        # Process the response as needed
    except botocore.exceptions.ClientError as e:
        logger.error(f"Error calling Lex V2: {e}")
        
def get_photo_path(keys):
    host = 'search-photos-orc4p7tbe7o6btwyt4l6xm4ugq.aos.us-east-1.on.aws'
    region = 'us-east-1'
    es_index = 'photos'

    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
    # awsauth = AWSRequestsAuth(aws_access_key='',
    #                   aws_secret_access_key='',
    #                   aws_host=host,
    #                   aws_region='us-east-1',
    #                   aws_service='es')
    
    # es = Elasticsearch(
    #     hosts=[{'host': host, 'port':443}],
    #     use_ssl=True,
    #     http_auth=awsauth,
    #     verify_certs=True,
    #     connection_class=RequestsHttpConnection)
        
    es = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )
        
    print("hoho")
    
    resp = []
    for key in keys:
        if (key is not None) and key != '':
            searchData = es.search({"query": {"match": {"labels": key}}})
            resp.append(searchData)
    print("response of open", resp)

    output = []
    for r in resp:
        if 'hits' in r:
             for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                if key not in output:
                    output.append('https://photos-bucket-3.s3.amazonaws.com/'+key,
                        )
    print ("outpout please", output)
    return output 




#################################################
# import json
# import math
# import dateutil.parser
# import datetime
# import time
# import os
# import logging
# import boto3

# import urllib.parse

# import random

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# headers = { "Content-Type": "application/json" }
# region = 'us-east-1'
# lex = boto3.client('lex-runtime', region_name=region)

# def lambda_handler(event, context):
#     # q1 = event["queryStringParameters"]["q"]
#     # labels = get_labels(q1)
#     q1 = "Trees and birds"    
#     # return q1
#     print("hello")
#     get_labels(q1)

    
# def get_labels(query):
#     sample_string = 'pqrstuvwxyabdsfbc'
#     userid = ''.join((random.choice(sample_string)) for x in range(8))
    
#     print(query)
#     print("hehehehehehheeheh")
    
#     response = lex.post_text(
#         botName='SearchPhotos',                 
#         botAlias='TestingAgainOne',
#         userId=userid,           
#         inputText=query
#     )
    
    
#     print("lex-response", response)
    
    