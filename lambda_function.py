# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import json
import urllib.parse
import boto3
import os

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])

        # Stream the file content directly into memory
        content = response['Body'].read().decode('utf-8')

        # Split into lines and modify first line
        lines = content.splitlines(keepends=True)
        if len(lines) > 0:
            print(f"First line of {key}: '{lines[0].strip()}'")
            lines[0] = "Hello World\n"
        else:
            lines = ["Hello World\n"]
        
        # Upload modified content back to S3
        s3.put_object(
            Bucket='myawsbucket-lambda-output', # to avoid potential recursive calling
            Key=key,
            Body=''.join(lines),
            Metadata=response.get('Metadata', {}),
            ContentType=response.get('ContentType', 'text/plain')
        )

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
