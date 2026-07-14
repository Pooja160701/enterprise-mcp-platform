import boto3
from botocore.exceptions import ClientError


class AWSService:

    def __init__(self):

        self.ec2 = boto3.client("ec2")

        self.s3 = boto3.client("s3")

        self.lambda_client = boto3.client("lambda")

        self.iam = boto3.client("iam")

        self.rds = boto3.client("rds")

        self.eks = boto3.client("eks")

        self.cloudwatch = boto3.client("cloudwatch")

    #
    # -------------------------
    # Health
    # -------------------------
    #

    def health(self):

        try:

            boto3.client("sts").get_caller_identity()

            return {
                "status": "healthy"
            }

        except Exception as e:

            return {
                "status": "offline",
                "error": str(e)
            }

    #
    # -------------------------
    # EC2
    # -------------------------
    #

    def list_instances(self):

        response = self.ec2.describe_instances()

        instances = []

        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:

                instances.append(
                    {
                        "id": instance["InstanceId"],
                        "state": instance["State"]["Name"],
                        "type": instance["InstanceType"],
                    }
                )

        return instances

    #
    # -------------------------
    # S3
    # -------------------------
    #

    def list_buckets(self):

        response = self.s3.list_buckets()

        return [
            {
                "name": bucket["Name"]
            }
            for bucket in response["Buckets"]
        ]

    #
    # -------------------------
    # Lambda
    # -------------------------
    #

    def list_lambda_functions(self):

        response = self.lambda_client.list_functions()

        return [
            {
                "name": fn["FunctionName"],
                "runtime": fn["Runtime"],
            }
            for fn in response["Functions"]
        ]

    #
    # -------------------------
    # IAM
    # -------------------------
    #

    def list_users(self):

        response = self.iam.list_users()

        return [
            {
                "name": user["UserName"]
            }
            for user in response["Users"]
        ]

    #
    # -------------------------
    # RDS
    # -------------------------
    #

    def list_rds_instances(self):

        response = self.rds.describe_db_instances()

        return [
            {
                "identifier": db["DBInstanceIdentifier"],
                "engine": db["Engine"],
                "status": db["DBInstanceStatus"],
            }
            for db in response["DBInstances"]
        ]

    #
    # -------------------------
    # EKS
    # -------------------------
    #

    def list_eks_clusters(self):

        response = self.eks.list_clusters()

        return response["clusters"]

    #
    # -------------------------
    # CloudWatch
    # -------------------------
    #

    def list_alarms(self):

        response = self.cloudwatch.describe_alarms()

        return [
            {
                "name": alarm["AlarmName"],
                "state": alarm["StateValue"],
            }
            for alarm in response["MetricAlarms"]
        ]