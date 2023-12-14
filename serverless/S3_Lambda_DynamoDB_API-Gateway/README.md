# Purpose: 
#### Create an API for returning company quarterly financial report using AWS Serverless Stack: S3, DynamoDB, Lambda and API Gateway

![image](https://github.com/srinivaskv1/aws_projects/assets/112094924/677db31a-d926-42d2-b5f9-b2adede54db8)
Note: Python 3.10 is used for Lambda functions.

**Assumptions:**
1) We will use AWS console for uploading quarterly finanical reports, in PDF format, to S3
2) Following folder structure will be used:
    Year
       Month
         Day
           Company
               Country

   See below image for the folder structure in S3
   ![image](https://github.com/srinivaskv1/aws_projects/assets/112094924/d04635e3-e27c-4431-a8fd-d7a0c04841df)

**Prerequisites:**
1) Local system with Python 10 for creating Lambda layer
2) Having AWS CLI and and SAM CLI will help in testing Lambda locally
   
**Configure DynamoDB table for storing Metadata**

**1) Create DynamoDB with partion key: company_quarter and sort key: country**
  ![image](https://github.com/srinivaskv1/aws_projects/assets/112094924/3978e590-2319-4a88-8338-2c8359901323)
  
 **2) Create local secondary index on geography. This can be used for getting items based on geography like Asia, Europe etc**
 ![image](https://github.com/srinivaskv1/aws_projects/assets/112094924/737d4376-821e-4cd0-b853-30e8a5b9a630)
 
 3) Table is used for storing the metadata associated with the objects stored in S3
 
**2) Create Lambda layer for DynamoDB Access**
  Lambda layer has been created for keeping Creating and querying DynamoDB table
  Steps for creating Lambda Layer. 
  
  2.1) Create a folder by name python in local system.
  
  2.2) Go to the newly created folder and install aws boto3
    ![image](https://github.com/srinivaskv1/aws_projects/assets/112094924/71f6234e-fca4-4029-81ba-beb463b4f505)
    
  2.3) Copy metadata_dynamo_layer.py in the same folder. The python code has 2 methods:
  
      a) updateMetadata: Creates new item in the DynamoDB table with the metadata including S3 file key. Here is sample data as stored in the DB
      ![image](https://github.com/srinivaskv1/aws_projects/assets/112094924/7d34a8c1-874c-45e3-8f31-0aa803af5fc3)

      b) getS3FileKey: Gets S3 file key stored in the dynamoDB based on Company, Quarter and Country

  2.4) Create zip for python folder
  2.5) Go to Lambda servie in AWS console. Click on layers for creating layer
  

  **3) Create Lambda functions**
5) Create S3 bucket and create Event Notifications for All Object Create Events

6) dd
