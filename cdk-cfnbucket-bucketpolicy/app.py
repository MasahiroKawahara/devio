#!/usr/bin/env python3

from aws_cdk import (
    core,
    aws_iam as iam,
    aws_s3 as s3,
)


class CfnBucketWithPolicyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = "cfn-bucket-with-policy-test-abcdefg"
        bucket_prefix = "alb-log"
        elb_account_id = "582318560864"

        # ポリシー作成
        policy_statement = iam.PolicyStatement()
        policy_statement.add_aws_account_principal(elb_account_id)
        policy_statement.add_actions("s3:PutObject")
        policy_statement.add_resources(
            "arn:aws:s3:::{0}/{1}/*".format(bucket_name, bucket_prefix))

        policy_document = iam.PolicyDocument(
            statements=[policy_statement]
        )

        # S3 バケット(CfnBucket)
        bucket = s3.CfnBucket(
            self, "Bucket",
            bucket_name=bucket_name
        )

        # バケットポリシー(CfnBucketPolicy)
        s3.CfnBucketPolicy(
            self, "BucketPolicy",
            bucket=bucket.ref,
            policy_document=policy_document.to_json()
        )


app = core.App()
CfnBucketWithPolicyStack(app, "CfnBucketWithPolicyStack")

app.synth()
