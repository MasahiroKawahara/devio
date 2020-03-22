from aws_cdk import core
from aws_cdk import aws_ec2 as ec2


class outNwStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Contexts
        PRJ = self.node.try_get_context("prj")
        CIDR_VPC = self.node.try_get_context("out-vpc-cidr")
        CIDR_NGW_SUBNET = self.node.try_get_context("out-ngw-subnet-cidr")
        CIDR_TGW_SUBNET = self.node.try_get_context("out-tgw-subnet-cidr")

        # Parameters
        # Functions
        def nametag(x): return core.CfnTag(
            key="Name", value="{}/{}".format(PRJ, x))

        # ### Resources
        # VPC
        self.vpc = ec2.CfnVPC(
            self, "vpc",
            cidr_block=CIDR_VPC,
            tags=[nametag("outVpc")]
        )
        # Ngw Subnet
        self.ngw_subnet = ec2.CfnSubnet(
            self, "ngwSubnet",
            cidr_block=CIDR_NGW_SUBNET,
            vpc_id=self.vpc.ref,
            map_public_ip_on_launch=False,
            availability_zone="ap-northeast-1a",
            tags=[nametag("outNgwSubnet")]
        )
        # Tgw Subnet
        self.tgw_subnet = ec2.CfnSubnet(
            self, "tgwSubnet",
            cidr_block=CIDR_TGW_SUBNET,
            vpc_id=self.vpc.ref,
            map_public_ip_on_launch=False,
            availability_zone="ap-northeast-1a",
            tags=[nametag("outTgwSubnet")]
        )
        # IGW
        self.igw = ec2.CfnInternetGateway(
            self, "igw",
            tags=[nametag("outIgw")]
        )
        igw_attachment = ec2.CfnVPCGatewayAttachment(
            self, "igwAttachment",
            vpc_id=self.vpc.ref,
            internet_gateway_id=self.igw.ref
        )
        # EIP for NATGW
        eip = ec2.CfnEIP(
            self, "eip",
            domain="vpc",
            tags=[nametag("outNatgwEip")]
        )
        eip.add_depends_on(igw_attachment)

        # NATGW
        self.natgw = ec2.CfnNatGateway(
            self, "natgw",
            allocation_id=eip.attr_allocation_id,
            subnet_id=self.ngw_subnet.ref,
            tags=[nametag("outNatgw")]
        )
        # RouteTable(NGW Subnet)
        self.ngw_rtb = ec2.CfnRouteTable(
            self, "ngwRtb",
            vpc_id=self.vpc.ref,
            tags=[nametag("outNgwRtb")]
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "ngwRtbAssoc",
            route_table_id=self.ngw_rtb.ref,
            subnet_id=self.ngw_subnet.ref
        )
        # RouteTable(TGW Subnet)
        self.tgw_rtb = ec2.CfnRouteTable(
            self, "tgwRtb",
            vpc_id=self.vpc.ref,
            tags=[nametag("outTgwRtb")]
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "tgwRtbAssoc",
            route_table_id=self.tgw_rtb.ref,
            subnet_id=self.tgw_subnet.ref
        )
