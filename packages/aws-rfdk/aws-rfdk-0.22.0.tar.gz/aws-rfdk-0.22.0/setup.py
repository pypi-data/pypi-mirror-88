import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-rfdk",
    "version": "0.22.0",
    "description": "Package for core render farm constructs",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-rfdk.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-rfdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_rfdk",
        "aws_rfdk._jsii",
        "aws_rfdk.deadline"
    ],
    "package_data": {
        "aws_rfdk._jsii": [
            "aws-rfdk@0.22.0.jsii.tgz"
        ],
        "aws_rfdk": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.assets==1.78.0",
        "aws-cdk.aws-apigateway==1.78.0",
        "aws-cdk.aws-applicationautoscaling==1.78.0",
        "aws-cdk.aws-autoscaling-common==1.78.0",
        "aws-cdk.aws-autoscaling-hooktargets==1.78.0",
        "aws-cdk.aws-autoscaling==1.78.0",
        "aws-cdk.aws-batch==1.78.0",
        "aws-cdk.aws-certificatemanager==1.78.0",
        "aws-cdk.aws-cloudformation==1.78.0",
        "aws-cdk.aws-cloudfront==1.78.0",
        "aws-cdk.aws-cloudwatch-actions==1.78.0",
        "aws-cdk.aws-cloudwatch==1.78.0",
        "aws-cdk.aws-codebuild==1.78.0",
        "aws-cdk.aws-codecommit==1.78.0",
        "aws-cdk.aws-codeguruprofiler==1.78.0",
        "aws-cdk.aws-codepipeline==1.78.0",
        "aws-cdk.aws-cognito==1.78.0",
        "aws-cdk.aws-docdb==1.78.0",
        "aws-cdk.aws-dynamodb==1.78.0",
        "aws-cdk.aws-ec2==1.78.0",
        "aws-cdk.aws-ecr-assets==1.78.0",
        "aws-cdk.aws-ecr==1.78.0",
        "aws-cdk.aws-ecs-patterns==1.78.0",
        "aws-cdk.aws-ecs==1.78.0",
        "aws-cdk.aws-efs==1.78.0",
        "aws-cdk.aws-elasticloadbalancing==1.78.0",
        "aws-cdk.aws-elasticloadbalancingv2==1.78.0",
        "aws-cdk.aws-events-targets==1.78.0",
        "aws-cdk.aws-events==1.78.0",
        "aws-cdk.aws-iam==1.78.0",
        "aws-cdk.aws-kinesis==1.78.0",
        "aws-cdk.aws-kms==1.78.0",
        "aws-cdk.aws-lambda==1.78.0",
        "aws-cdk.aws-logs==1.78.0",
        "aws-cdk.aws-route53-targets==1.78.0",
        "aws-cdk.aws-route53==1.78.0",
        "aws-cdk.aws-s3-assets==1.78.0",
        "aws-cdk.aws-s3==1.78.0",
        "aws-cdk.aws-sam==1.78.0",
        "aws-cdk.aws-secretsmanager==1.78.0",
        "aws-cdk.aws-servicediscovery==1.78.0",
        "aws-cdk.aws-sns-subscriptions==1.78.0",
        "aws-cdk.aws-sns==1.78.0",
        "aws-cdk.aws-sqs==1.78.0",
        "aws-cdk.aws-ssm==1.78.0",
        "aws-cdk.aws-stepfunctions==1.78.0",
        "aws-cdk.cloud-assembly-schema==1.78.0",
        "aws-cdk.core==1.78.0",
        "aws-cdk.custom-resources==1.78.0",
        "aws-cdk.cx-api==1.78.0",
        "aws-cdk.region-info==1.78.0",
        "constructs>=3.2.0, <4.0.0",
        "jsii>=1.16.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
