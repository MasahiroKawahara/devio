from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from stacks.tgwStack import tgwStack


class tgwRouteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, tgw_stack: tgwStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Contexts
        PRJ = self.node.try_get_context("prj")
        CHILD_TGW_ATTACHMENT_ID = self.node.try_get_context(
            "child-tgw-attachment-id")
        CHILD_VPC_CIDR = self.node.try_get_context("child-vpc-cidr")

        # Parameters
        # Functions
        def nametag(x): return core.CfnTag(
            key="Name", value="{}/{}".format(PRJ, x))

        # ### Resources
        # Route table
        self.default_tgw_rtb = ec2.CfnTransitGatewayRouteTable(
            self, "tgwRtb",
            transit_gateway_id=tgw_stack.tgw.ref,
            tags=[nametag("tgwRtb")]
        )
        # Route table associations
        associations = [
            # (ResourceId, TgwAttachmentId)
            ("tgwRtbAssocForOutboundVpc", tgw_stack.out_tgw_attachment.ref),
            ("tgwRtbAssocForAppVpc", CHILD_TGW_ATTACHMENT_ID)
        ]
        for resource_id, tgw_att_id in associations:
            ec2.CfnTransitGatewayRouteTableAssociation(
                self, resource_id,
                transit_gateway_attachment_id=tgw_att_id,
                transit_gateway_route_table_id=self.default_tgw_rtb.ref
            )
        # Routes
        routes = [
            # (ResourceId, DestinationCidr, TgwAttachmentId)
            ("tgwRouteOutbound", "0.0.0.0/0", tgw_stack.out_tgw_attachment.ref),
            ("tgwRouteApp", CHILD_VPC_CIDR, CHILD_TGW_ATTACHMENT_ID)
        ]
        for resource_id, cidr, tgw_att_id in routes:
            ec2.CfnTransitGatewayRoute(
                self, resource_id,
                transit_gateway_route_table_id=self.default_tgw_rtb.ref,
                destination_cidr_block=cidr,
                transit_gateway_attachment_id=tgw_att_id
            )
