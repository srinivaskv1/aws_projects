import json
import urllib.parse
import boto3
import metadata_dynamo_layer as metadata

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        print("Key =>"+key)
        response = s3.get_object(Bucket=bucket, Key=key)

        key_list = key.split("/")
        # Key size is considered as 5 as the metadata needs to be captured for files stored in the folder:
        # s3://mydemorepository/<<YEAR>>/<<Quareter like 01,02,03,04>>/<<Company Name like amazon, IBM>>/<<Country like US, UK, IN>>/
        if (len(key_list) == 5) :
            year_str = key_list[0]
            month_str = key_list[1]
            company_str = key_list[2]
            country_str = key_list[3]
            
            # create metadata record in dynamodb table
            print("Metadata update Status => ",metadata.updateMetadata(company_str, year_str.strip()+month_str.strip(), country_str,key))
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
