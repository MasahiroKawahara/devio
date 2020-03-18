#!/usr/bin/env python3

from aws_cdk import core

from stacks.appNwStack import appNwStack
from stacks.appInstance import appInstanceStack
from stacks.outNwStack import outNwStack
from stacks.tgwStack import tgwStack
from stacks.tgwRouteStack import tgwRouteStack
from stacks.vpcRouteStack import vpcRouteStack


app = core.App()

PRJ = app.node.try_get_context("prj")

app_nw_stack = appNwStack(app, PRJ + "AppNwStack")
app_instance_stack = appInstanceStack(
    app, PRJ + "AppInstanceStack", app_nw_stack)
out_nw_stack = outNwStack(app, PRJ + "OutNwStack")
tgw_stack = tgwStack(app, PRJ + "TgwStack", app_nw_stack, out_nw_stack)

tgw_route_stack = tgwRouteStack(
    app, PRJ + "TgwRouteStack", tgw_stack
)
vpc_route_stack = vpcRouteStack(
    app, PRJ + "VpcRouteStack", app_nw_stack, out_nw_stack, tgw_stack)


app.synth()
