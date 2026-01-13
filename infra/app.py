#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.ecs_stack import RiamLmsStack


app = cdk.App()

# Get account from environment or use default
account = app.node.try_get_context("account") or "682190641149"
region = app.node.try_get_context("region") or "us-west-2"

RiamLmsStack(
    app,
    "RiamLmsStack",
    description="RIAM Learning Management System API Stack",
    env=cdk.Environment(account=account, region=region),
)

app.synth()
