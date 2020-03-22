from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from stacks.outNwStack import outNwStack


class tgwStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, out_nw_stack: outNwStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Contexts
        PRJ = self.node.try_get_context("prj")

        # Parameters
        # Functions
        def nametag(x): return core.CfnTag(
            key="Name", value="{}/{}".format(PRJ, x))

        # ### Resources
        # Tgw
        self.tgw = ec2.CfnTransitGateway(
            self, "tgw",
            auto_accept_shared_attachments="enable",
            default_route_table_association="disable",
            default_route_table_propagation="disable",
            description="transit gateway({})".format(PRJ),
            tags=[nametag("tgw")]
        )
        # Tgw Attachment for Outbound-VPC
        self.out_tgw_attachment = ec2.CfnTransitGatewayAttachment(
            self, "outTgwAttachment",
            vpc_id=out_nw_stack.vpc.ref,
            subnet_ids=[out_nw_stack.tgw_subnet.ref],
            transit_gateway_id=self.tgw.ref,
            tags=[nametag("outTgwAttachment")]
        )
