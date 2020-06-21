#!/usr/bin/env python3

from aws_cdk import core

from sample_cdk_new.sample_cdk_new_stack import SampleCdkNewStack


app = core.App()
SampleCdkNewStack(app, "sample-cdk-new", env={'region': 'cn-north-1'})

app.synth()
