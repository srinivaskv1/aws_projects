# Steps for creating EC2 instance in the private subnet of existing VPC
1) We may use the VPC created earlier with CDK and add necessary code to create EC2 instance in the private subnet
2) We need Amazon Linux AMI for creating VPC. Below code blokc determines AMI ID
  
  ```
     amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )
  ```
3) Create Role for assigning to EC2 instance with SSM polocy
   
  ```
         role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
  ```

4) Add SSM Managed Policy to the role
    
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

5) Create the t3 Nano instance in the private subnet

  ```
      instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=amzn_linux,
            vpc = myVpc,
            role = role,
            vpc_subnets=ec2.SubnetSelection(subnets=myVpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets),
            user_data=
            )
  ```

6) Follow the deployment steps for creating EC2 instance in the private subnet of VPC

6.1) Execute synth command

  `cdk synth`
  
6.2) Deploy the updated stack

  `cdk deploy`

  ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/b2d33503-3f17-4b46-bd42-82cd7f4e9e94)

  Confirm for deploying the stack

  ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/6d2d7161-ffd7-4303-84af-a1623bddb2c0)

  Check the Cloudformation stacks in the console

  ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/72ac4212-7688-4393-b080-f63ce70e6c62)

  ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/a56979c6-6a61-4f6e-92e6-843236cefdba)

  Check the instance information:

  ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/996134a7-67f8-476a-b583-1d974e9cfab8)

  ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/f3436455-9fc8-4f20-828e-b153ca308ddf)

  Check the IAM role

  ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/8afa95be-d337-4c38-9d18-32fa3791e0db)

7) Excure destroy for removing the newly created stack
   
  `cdk destroy`

  ![image](https://github.com/srinivaskv1/awsprojects/assets/112094924/c20c8578-e195-4384-9ce9-e84c458d71d1)









