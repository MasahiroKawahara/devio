from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from stacks.appNwStack import appNwStack


class tgwAttachmentStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, app_nw_stack: appNwStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Contexts
        PRJ = self.node.try_get_context("prj")
        TGW_ID = self.node.try_get_context("tgw-id")

        # Parameters
        # Functions
        def nametag(x): return core.CfnTag(
            key="Name", value="{}/{}".format(PRJ, x))

        # ### Resources
        # Tgw Attachment for APP-VPC
        self.out_tgw_attachment = ec2.CfnTransitGatewayAttachment(
            self, "appTgwAttachment",
            vpc_id=app_nw_stack.vpc.ref,
            subnet_ids=[app_nw_stack.tgw_subnet.ref],
            transit_gateway_id=TGW_ID,
            tags=[nametag("appTgwAttachment")]
        )
        # ### Output
        core.CfnOutput(
            self, "tgwAttachmentOutput",
            value=self.out_tgw_attachment.ref,
            export_name="TgwAttachmentId"
        )
