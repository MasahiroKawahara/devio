from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from stacks.tgwStack import tgwStack
from stacks.outNwStack import outNwStack


class vpcRouteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, out_nw_stack: outNwStack, tgw_stack: tgwStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # contexts
        PRJ = self.node.try_get_context("prj")
        CHILD_VPC_CIDR = self.node.try_get_context("child-vpc-cidr")

        # ### Resources
        # Routes for Natgw subnet
        ec2.CfnRoute(
            self, "outNgwRouteDefault",
            route_table_id=out_nw_stack.ngw_rtb.ref,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=out_nw_stack.igw.ref
        )
        child_vpc_cidrs = [
            # (resource_id, cidr)
            ("outNgwRoute1", CHILD_VPC_CIDR)
        ]
        for resource_id, cidr in child_vpc_cidrs:
            ec2.CfnRoute(
                self, resource_id,
                route_table_id=out_nw_stack.ngw_rtb.ref,
                destination_cidr_block=cidr,
                transit_gateway_id=tgw_stack.tgw.ref
            )
        # Route for Tgw Subnet
        ec2.CfnRoute(
            self, "outTgwRouteDefault",
            route_table_id=out_nw_stack.tgw_rtb.ref,
            destination_cidr_block="0.0.0.0/0",
            nat_gateway_id=out_nw_stack.natgw.ref
        )
