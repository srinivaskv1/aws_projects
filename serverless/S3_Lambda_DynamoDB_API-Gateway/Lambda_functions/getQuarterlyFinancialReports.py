import json
import os
import boto3
import base64
import metadata_dynamo_layer as metadata

from boto3.dynamodb.conditions import Key, Attr

s3 = boto3.client('s3')

def getRequestParameter(event,strKey) :
    try :
        return event["queryStringParameters"][strKey]
    except :
        return ""
    
def getPathParameter(event,strKey) :
    try :
         return event["pathParameters"][strKey]
    except :
         return ""

def lambda_handler(event, context):
    company = getRequestParameter(event,"company")
    quarter=getRequestParameter(event,"quarter")
    country=getRequestParameter(event,"country")
    print("Request Parameters :: Company : "+company +" :: "+ "Quarter : "+quarter + " :: Country :"+country )

    try :
        try :
            s3_bucket = os.environ.get('mydemorepository')
        except :
            raise Exception("Required Environment Variables are not set")
        
        if (company == "" or quarter == "" or country == "") :
            raise Exception("Invalid Query Parameters:: Company: "+company +" :: "+ "Quarter : "+quarter + " :: Country :"+country )
            
        s3FileKey = metadata.getS3FileKey(company, quarter, country)

        if s3FileKey == "" :
            raise Exception("Report not found for the criteria:: Company: "+company +" :: "+ "Quarter : "+quarter + " :: Country :"+country )
            
        fileObject = s3.get_object(
                Bucket=s3_bucket,
                Key=s3FileKey,
            )

        pdf_content = fileObject["Body"].read()
    
        return {
                "statusCode": 200,
                "headers": {
                        "Content-Type": "application/pdf",
                        "Content-Disposition": "attachment; filename=text.pdf",
                },
                "body": base64.b64encode(pdf_content),
                "isBase64Encoded": True,
        }

    except Exception as error:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "Message ": str(error)
            })
        }
