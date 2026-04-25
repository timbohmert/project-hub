#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.infra_stack import InfraStack


app = cdk.App()
InfraStack(app, "ProjectHubStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'), 
        region='us-east-1'
    ),
)

app.synth()
