from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_cloudwatch as cloudwatch,
    aws_sns as sns,
    aws_lambda as flambda,
    aws_sns_subscriptions as sub

)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        error_metric= cloudwatch.Metric(
            namespace = 'AWS/Lambda',
            metric_name = 'Errors',
            dimensions_map= {'FunctionName': 'Test'},
            statistics= 'sum',
            period=Duration.minutes(5)   
        )

        alarm = cloudwatch.Alarm(self,
                                 "LambdaAlarm",
                                 metric=error_metric,
                                 threshold=1,
                                 evaluation_periods=1,
                                 alarm_description="If lambda has errors")
        
        alert_sns= sns.Topic(self, "AlertTopic")
        alarm.add_alarm_action(actions.SnsAction(alert_sns))




