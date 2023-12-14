#!/usr/bin/env python3
import boto3

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

dynamoTable = dynamodb.Table('metadata_s3_demo')

def updateMetadata(companyStr, quarterStr, countryStr,keyStr) :
    dynamoStatus = dynamoTable.put_item(
        Item={
                'company_quarter': companyStr.strip() +  "_" + quarterStr.strip(),
                'country': countryStr.strip(),
                'key': keyStr.strip()
        }
    )
    return dynamoStatus

def getS3FileKey(companyStr, quarterStr, countryStr) :
    companyQtrStr = companyStr.strip() + "_" + quarterStr.strip()
    print("Query Conditions ==> "+companyQtrStr + " :: "+countryStr + " :: Expected = "+"amazon_202301")

    try :
        queryResponse = dynamoTable.query(
            KeyConditionExpression="company_quarter = :id and country = :ct",
            ExpressionAttributeValues={
                ":id": companyQtrStr,
                ":ct": countryStr,
            },
        )
        print("Query Response")
        print(queryResponse)
        s3FileKey = queryResponse['Items'][0]['key']
        print("Key =====> "+ s3FileKey)
        return s3FileKey
    except :
        print("Invalid S3 key : "+  companyQtrStr + "_" + countryStr)
        return ""
    
#test the function
myFileKey = getS3FileKey("amazon","202301","US")
print("returned file key :: " +myFileKey)
        
