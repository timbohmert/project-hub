from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm,
)
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        domain_name = "timbohmert.com"

        # 1. Lookup the Hosted Zone we created earlier
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name=domain_name
        )

        # 2. Create an SSL Certificate (ACM)
        certificate = acm.DnsValidatedCertificate(
            self, "SiteCertificate",
            domain_name=domain_name,
            hosted_zone=hosted_zone,
            region="us-east-1", # CloudFront requires us-east-1
            subject_alternative_names=[f"www.{domain_name}"]
        )

        # 3. S3 Bucket for the static site
        site_bucket = s3.Bucket(
            self, "SiteBucket",
            bucket_name=f"{domain_name}-content",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        # 4. CloudFront Distribution
        distribution = cloudfront.Distribution(
            self, "SiteDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(site_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            domain_names=[domain_name, f"www.{domain_name}"],
            certificate=certificate,
            default_root_object="index.html",
            # Handle SPA routing (redirect 404s to index.html)
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0)
                )
            ]
        )

        # 5. Route 53 A Records to point to CloudFront
        route53.ARecord(
            self, "SiteAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
            record_name=domain_name
        )

        route53.ARecord(
            self, "WWWAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
            record_name=f"www.{domain_name}"
        )
