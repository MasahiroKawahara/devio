from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from stacks.appNwStack import appNwStack


class vpcRouteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, app_nw_stack: appNwStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # contexts
        PRJ = self.node.try_get_context("prj")
        TGW_ID = self.node.try_get_context("tgw-id")

        # ### Resources
        # App: Tgw Subnet Route --> no route required
        # App: App Subnet Route
        ec2.CfnRoute(
            self, "appEc2Route1",
            route_table_id=app_nw_stack.ec2_rtb.ref,
            destination_cidr_block="0.0.0.0/0",
            transit_gateway_id=TGW_ID
        )
