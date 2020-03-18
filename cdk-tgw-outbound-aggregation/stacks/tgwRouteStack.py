from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from stacks.tgwStack import tgwStack


class tgwRouteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, tgw_stack: tgwStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Contexts
        PRJ = self.node.try_get_context("prj")
        CIDR_APP_VPC = self.node.try_get_context("cidr-app-vpc")

        # Parameters
        # Functions
        def nametag(x): return core.CfnTag(
            key="Name", value="{}/{}".format(PRJ, x))

        # ### Resources
        # Tgw Route (rtb_default: 0.0.0.0 --> Outbound VPC)
        ec2.CfnTransitGatewayRoute(
            self, "defaultTgwRoute1",
            transit_gateway_route_table_id=tgw_stack.default_tgw_rtb.ref,
            destination_cidr_block="0.0.0.0/0",
            transit_gateway_attachment_id=tgw_stack.out_tgw_attachment.ref
        )
        # Tgw Route (rtb_default: APP_CIDR --> App1 VPC)
        ec2.CfnTransitGatewayRoute(
            self, "defaultTgwRoute2",
            transit_gateway_route_table_id=tgw_stack.default_tgw_rtb.ref,
            destination_cidr_block=CIDR_APP_VPC,
            transit_gateway_attachment_id=tgw_stack.app_tgw_attachment.ref
        )
