from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from stacks.tgwStack import tgwStack
from stacks.appNwStack import appNwStack
from stacks.outNwStack import outNwStack


class vpcRouteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, app_nw_stack: appNwStack, out_nw_stack: outNwStack, tgw_stack: tgwStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # contexts
        PRJ = self.node.try_get_context("prj")
        CIDR_APP_VPC = self.node.try_get_context("cidr-app-vpc")

        # ### Resources
        # App1: Tgw Subnet Route --> no route required
        # App1: App Subnet Route
        ec2.CfnRoute(
            self, "appEc2Route1",
            route_table_id=app_nw_stack.ec2_rtb.ref,
            destination_cidr_block="0.0.0.0/0",
            transit_gateway_id=tgw_stack.tgw.ref
        )
        # Out: Natgw Subnet Route
        ec2.CfnRoute(
            self, "outNgwRoute1",
            route_table_id=out_nw_stack.ngw_rtb.ref,
            destination_cidr_block=CIDR_APP_VPC,
            transit_gateway_id=tgw_stack.tgw.ref
        )
        ec2.CfnRoute(
            self, "outNgwRoute2",
            route_table_id=out_nw_stack.ngw_rtb.ref,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=out_nw_stack.igw.ref
        )
        # Out: Tgw Subnet Route
        ec2.CfnRoute(
            self, "outTgwRoute1",
            route_table_id=out_nw_stack.tgw_rtb.ref,
            destination_cidr_block="0.0.0.0/0",
            nat_gateway_id=out_nw_stack.natgw.ref
        )
