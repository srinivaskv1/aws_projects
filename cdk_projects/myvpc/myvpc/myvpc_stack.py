from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class MyvpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # vpc
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
                    cidr_mask = 24,
                )
            ],
            nat_gateways=1,    
         )
        # Adding an ec2 instance to private subnet

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )

        #private_subnets = [subnet.subnet_id for subnet in myVpc.private_subnets]
        
        #https://aws.amazon.com/blogs/mt/applying-managed-instance-policy-best-practices/
        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Instance
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=amzn_linux,
            vpc = myVpc,
            role = role,
            vpc_subnets=ec2.SubnetSelection(subnets=myVpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets),
            )


