from aws_cdk import (
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda as awslambda,
    aws_cloudwatch as cw,
    core
)
from os import path
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import LambdaFunction

class SampleCdkNewStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        mytopic = sns.Topic(
            self, "BillingAlert"
        )

        email_parameter = core.CfnParameter(self, "email-param")
        dailyBudget_parameter = core.CfnParameter(self, "DailyBudget")
        monthlyGrowthRate_parameter = core.CfnParameter(self, "MonthlyGrowthRate")
        S3CodePath_parameter = core.CfnParameter(self, "S3CodePath")

        emailAddress = getattr(email_parameter,"value_as_string")
        dailyBudget_value = getattr(dailyBudget_parameter,"value_as_string")
        monthlyGrowthRate_value = getattr(monthlyGrowthRate_parameter,"value_as_string")

        mytopic.add_subscription(subscriptions.EmailSubscription(emailAddress))
        myrole = iam.Role(self, "BillianAlertRole", assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        myrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"))
        myrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaBasicExecutionRole"))
        myrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess "))

        function = awslambda.Function(self, "MyLambda",
            code=awslambda.Code.from_cfn_parameters(object_key_param=S3CodePath_parameter),
            handler="lambda_function.py",
            runtime=awslambda.Runtime.PYTHON_3_7,
            role = myrole,
            function_name= "BillingAlert",
            memory_size= 3000
            )
        function.add_environment("DailyBudget", dailyBudget_value)
        function.add_environment("MonthlyGrowthRate", monthlyGrowthRate_value)
        function.add_environment("SNSARN", getattr(mytopic,"topic_arn"))
        targetFunction = LambdaFunction(function)
        Rule(self, "ScheduleRuleForBillingAlert",
            schedule=Schedule.cron(minute="0", hour="4"),
            targets=[targetFunction]
        )
