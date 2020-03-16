#!/usr/bin/env python3

from aws_cdk import core

from stacks.appNwStack import appNwStack
from stacks.outNwStack import outNwStack
from stacks.tgwStack import tgwStack
from stacks.vpcRouteStack import vpcRouteStack
from stacks.appInstance import appInstanceStack

app = core.App()

app_nw_stack = appNwStack(app, "AppNwStack")
out_nw_stack = outNwStack(app, "OutNwStack")
tgw_stack = tgwStack(app, "TgwStack", app_nw_stack, out_nw_stack)
vpc_route_stack = vpcRouteStack(
    app, "vpcRouteStack", app_nw_stack, out_nw_stack, tgw_stack)
app_instance_stack = appInstanceStack(app, "AppInstanceStack", app_nw_stack)

app.synth()
