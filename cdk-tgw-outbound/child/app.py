#!/usr/bin/env python3

from aws_cdk import core

from stacks.appNwStack import appNwStack
from stacks.appInstanceStack import appInstanceStack
from stacks.vpcRouteStack import vpcRouteStack
from stacks.tgwAttachment import tgwAttachmentStack

app = core.App()

PRJ = app.node.try_get_context("prj")

app_nw_stack = appNwStack(app, PRJ + "AppNwStack")
app_instance_stack = appInstanceStack(
    app, PRJ + "AppInstanceStack", app_nw_stack)

# Check if "tgw-id" is correct in cdk.json before deploy
tgw_att_stack = tgwAttachmentStack(
    app, PRJ + "TgwAttachmentStack", app_nw_stack)
vpc_route_stack = vpcRouteStack(app, PRJ + "VpcRouteStack", app_nw_stack)

app.synth()
