from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from stacks.appNwStack import appNwStack


class appInstanceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, app_nw_stack: appNwStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Contexts
        PRJ = self.node.try_get_context("prj")
        AMI_ID = self.node.try_get_context("ami-id")  # Amazon Linux 2

        # Functions
        def nametag(x): return core.CfnTag(
            key="Name", value="{}/{}".format(PRJ, x))

        # ### Resources
        # IAM Role
        ec2_statement = iam.PolicyStatement()
        ec2_statement.add_actions("sts:AssumeRole")
        ec2_statement.add_service_principal(service="ec2.amazonaws.com")
        ec2_document = iam.PolicyDocument(
            statements=[ec2_statement]
        )
        iam_role = iam.CfnRole(
            self, "iamRoleForEc2",
            role_name="{}-ec2-role".format(PRJ),
            description="{}-ec2-role".format(PRJ),
            assume_role_policy_document=ec2_document.to_json(),
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
            ]
        )
        ec2_instance_profile = iam.CfnInstanceProfile(
            self, "ec2InstanceProfile",
            roles=[iam_role.ref],
            instance_profile_name="{}-ec2-instance-profile".format(PRJ)
        )
        # Security Group
        sg = ec2.CfnSecurityGroup(
            self, "sg",
            group_description="sg for ec2 instance({})".format(PRJ),
            vpc_id=app_nw_stack.vpc.ref
        )
        # Instance
        ec2.CfnInstance(
            self, "instance",
            iam_instance_profile=ec2_instance_profile.ref,
            image_id=AMI_ID,
            instance_type="t3.micro",
            security_group_ids=[sg.ref],
            subnet_id=app_nw_stack.ec2_subnet.ref,
            tags=[nametag("instance")]
        )
