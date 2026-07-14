from service import AWSService

aws = AWSService()

print("\nHealth\n")
print(aws.health())

print("\nEC2\n")
print(aws.list_instances())

print("\nS3\n")
print(aws.list_buckets())

print("\nLambda\n")
print(aws.list_lambda_functions())

print("\nIAM\n")
print(aws.list_users())

print("\nRDS\n")
print(aws.list_rds_instances())

print("\nEKS\n")
print(aws.list_eks_clusters())

print("\nCloudWatch\n")
print(aws.list_alarms())