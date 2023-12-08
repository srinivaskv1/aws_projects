# Steps for creating VPC with AWS CDK 
> **Note**: Below steps are followed for creating CDK project in Windows environment
## Prerequisites
1) Install and configure AWS CLI. Below command gives default account configurred
   
   `_aws sts get-caller-identity_`

    **Output:**

    _{
        "UserId": "121212121212",
        "Account": "12345678900",
        "Arn": "arn:aws:iam::12345678900:root"
    }_

3) Install Nod JS
4) Install the AWS CDK Toolkit globally using the following Node Package Manager command.
   
    `_npm install -g aws-cdk_`
   
    Below command gives CDK version
   
    `_cdk --version_`
5) Deploying stacks with the AWS CDK requires dedicated Amazon S3 buckets and other containers to be available to AWS CloudFormation during deployment. Creating these is called bootstrapping. To bootstrap, issue:
   
    `_cdk bootstrap aws://ACCOUNT-NUMBER/REGION_`
   
## Create CDK Project for VPC
1) Create a folder
    _md myvpc_
   
2) Go to the newly created folder 
    _cd myvpc_

3) Initialize the python project
   
    `cdk init --language python`

    Successful execution of above command creates set of folders and files:

   ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/1ad5eb3d-c57c-4ee9-a540-58091cc21128)

5) The requirements.txt (see below) created during project initilization is sufficient for this project.
   
    ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/1b55ce82-6e26-4e0c-941c-b313f502c76c)

7) Install the required packages 

    `pip3 install -r requirements.txt`

## Update Source for creating VPC
1) CDK project initializtion (Step #3 in Create CDK Porject for VPC section), creates ProjectFolerName_stack.py like **myvpc_stack.py**. The file needs to be updated with required stack information. The stack will be executed by **app.py**
2) Below is the modified **myvpc_stack.py**
   
   `from aws_cdk import (
       aws_ec2 as ec2,
       Stack,
   )
   from constructs import Construct
   
   class MyvpcStack(Stack):
   
       def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
           super().__init__(scope, construct_id, **kwargs)
   
           # The code that defines your stack goes here
   
           # vpc requirements:
           # name: myVPC, Cidr: 10.0.0.0/16
           # Subnets: 1 public and 1 private with cidr mask = 24
           # Note: CIDR range cannot be specified for subnets
           
           myVpc = ec2.Vpc(self, "myVpc",
               ip_addresses=ec2.IpAddresses.cidr('10.0.0.0/16'),
               max_azs = 1,
               enable_dns_hostnames = True,
               enable_dns_support = True, 
               subnet_configuration=[
                   ec2.SubnetConfiguration(
                       name = 'public',
                       subnet_type = ec2.SubnetType.PUBLIC,
                       cidr_mask = 24
                   ),
                   ec2.SubnetConfiguration(
                       name = 'private',
                       subnet_type = ec2.SubnetType.PRIVATE_WITH_EGRESS,
                       cidr_mask = 24
                   )
               ],
               nat_gateways=1,    
            )

## Create VPC stack in the configured AWS Account
1) Execute below command in the prject folder **myvpc** for synthesising CDK app code into a CloudFormation stack
   
   `cdk synth`
   
   Above commands outpus cloudformation stack
   
2) Execute Deploy command for deploying the stack

   `cdk deploy`

   Dispalays the stacks that will be created and prompts for confirmation. Enter y for deploying the stacks in the AWS account.
   
3) Infrastructure stacks will be created and they will appear in Cloudformation

   ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/0a2562e5-88d1-49f3-b6da-119f254becc5)

   ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/50b78e3b-c78b-4363-ada4-f79db200f35d)


## Cleanup the stack
Execute below command to delete from the same project folder for deleting the stacks

`cdk destroy`

Prompts for the confirmation.

![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/4e9b852e-db20-4df5-9ec9-5d687b00ffd9)

Below message will be displayed after destroying the stacks

![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/d7cc4a68-2355-4b6a-9a68-f77410082f55)








