#!/usr/bin/env python3

from aws_cdk import core
from stacks.outNwStack import outNwStack
from stacks.tgwStack import tgwStack
from stacks.tgwRouteStack import tgwRouteStack
from stacks.vpcRouteStack import vpcRouteStack

app = core.App()

PRJ = app.node.try_get_context("prj")

out_nw_stack = outNwStack(app, PRJ + "OutNwStack")
tgw_stack = tgwStack(app, PRJ + "TgwStack", out_nw_stack)

vpc_route_stack = vpcRouteStack(
    app, PRJ + "VpcRouteStack", out_nw_stack, tgw_stack)

# Check if "child-tgw-attachment-id" is correct value in cdk.json before deploy
tgw_route_stack = tgwRouteStack(
    app, PRJ + "TgwRouteStack", tgw_stack)

app.synth()
