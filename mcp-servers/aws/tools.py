from service import AWSService

service = AWSService()


def health():
    return service.health()


def list_ec2_instances():
    return service.list_instances()


def list_s3_buckets():
    return service.list_buckets()


def list_lambda_functions():
    return service.list_lambda_functions()


def list_iam_users():
    return service.list_users()


def list_rds_instances():
    return service.list_rds_instances()


def list_eks_clusters():
    return service.list_eks_clusters()


def list_cloudwatch_alarms():
    return service.list_alarms()