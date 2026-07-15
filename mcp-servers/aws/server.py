from mcp.server.fastmcp import FastMCP

from tools import (
    health,
    list_ec2_instances,
    list_s3_buckets,
    list_lambda_functions,
    list_iam_users,
    list_rds_instances,
    list_eks_clusters,
    list_cloudwatch_alarms,
)

mcp = FastMCP("AWS MCP")


@mcp.tool()
def health_tool():
    """Check AWS connectivity."""
    return health()


@mcp.tool()
def list_ec2_instances_tool():
    """List EC2 instances."""
    return list_ec2_instances()


@mcp.tool()
def list_s3_buckets_tool():
    """List S3 buckets."""
    return list_s3_buckets()


@mcp.tool()
def list_lambda_functions_tool():
    """List Lambda functions."""
    return list_lambda_functions()


@mcp.tool()
def list_iam_users_tool():
    """List IAM users."""
    return list_iam_users()


@mcp.tool()
def list_rds_instances_tool():
    """List RDS instances."""
    return list_rds_instances()


@mcp.tool()
def list_eks_clusters_tool():
    """List EKS clusters."""
    return list_eks_clusters()


@mcp.tool()
def list_cloudwatch_alarms_tool():
    """List CloudWatch alarms."""
    return list_cloudwatch_alarms()


if __name__ == "__main__":
    mcp.run()