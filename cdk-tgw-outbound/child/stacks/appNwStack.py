from aws_cdk import core
from aws_cdk import aws_ec2 as ec2


class appNwStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Contexts
        PRJ = self.node.try_get_context("prj")
        CIDR_VPC = self.node.try_get_context("cidr-app-vpc")
        CIDR_APP_SUBNET = self.node.try_get_context("cidr-app-ec2-subnet")
        CIDR_TGW_SUBNET = self.node.try_get_context("cidr-app-tgw-subnet")

        # Parameters
        # Functions
        def nametag(x): return core.CfnTag(
            key="Name", value="{}/{}".format(PRJ, x))

        # ### Resources
        # VPC
        self.vpc = ec2.CfnVPC(
            self, "vpc",
            cidr_block=CIDR_VPC,
            tags=[nametag("appVpc")]
        )
        # Ec2 Subnet
        self.ec2_subnet = ec2.CfnSubnet(
            self, "ec2Subnet",
            cidr_block=CIDR_APP_SUBNET,
            vpc_id=self.vpc.ref,
            map_public_ip_on_launch=False,
            availability_zone="ap-northeast-1a",
            tags=[nametag("appEc2Subnet")]
        )
        # Tgw Subnet
        self.tgw_subnet = ec2.CfnSubnet(
            self, "tgwSubnet",
            cidr_block=CIDR_TGW_SUBNET,
            vpc_id=self.vpc.ref,
            map_public_ip_on_launch=False,
            availability_zone="ap-northeast-1a",
            tags=[nametag("appTgwSubnet")]
        )
        # RouteTable(App Subnet)
        self.ec2_rtb = ec2.CfnRouteTable(
            self, "ec2Rtb",
            vpc_id=self.vpc.ref,
            tags=[nametag("appEc2Rtb")]
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "ec2RtbAssoc",
            route_table_id=self.ec2_rtb.ref,
            subnet_id=self.ec2_subnet.ref
        )

        # RouteTable(Tgw Subnet)
        self.tgw_rtb = ec2.CfnRouteTable(
            self, "tgwRtb",
            vpc_id=self.vpc.ref,
            tags=[nametag("appTgwRtb")]
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "tgwRtbAssoc",
            route_table_id=self.tgw_rtb.ref,
            subnet_id=self.tgw_subnet.ref
        )
